import atexit
import csv
import inspect
import json
import logging
import os
import signal
import sys
import time
import click
import panapi
from panapi.config import \
    iam, \
    security, \
    identity, \
    objects, \
    network, \
    subscription, \
    tenancy, \
    mobile

__author__ = "Palo Alto Networks"
__copyright__ = "Copyright 2023, Palo Alto Networks"
__credits__ = ["Robert Hagen", "Anton Coleman"]
__license__ = "MIT"
__version__ = ".2"
__maintainer__ = "Anton Coleman"
__email__ = "acoleman@paloaltonetworks.com"
__status__ = "Community"


# TODO Add Exception Handling


def setup_logger(logger_name, log_file, file_level=logging.DEBUG, stream_level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setLevel(file_level)
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(stream_level)
    streamHandler.setFormatter(formatter)
    l.setLevel(logging.DEBUG)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)
    return l


logger = setup_logger('config_logger', 'config_exporter.log', file_level=logging.DEBUG,
                      stream_level=logging.INFO)


def create_session():
    """

    Returns: Session Object

    """
    try:
        logger.info(f'Generating new session')
        session = panapi.PanApiSession()
        session.authenticate()
        logger.info(f'Session Generated')
        time.sleep(1)
        return session
    except Exception as e:
        logger.critical(f'Failed with exception: {e}')
        return f'Failed with exception: {e}'


############################################################
# Checks for matching rule IDs between positional rulebases
############################################################
def cleanup_duplicate_rules(folders, rules):
    """
        Args:
            folders: List of Prisma Access folders to cycle through
            rules: Dictionary of rules generated from the get_rules() function
    """
    try:
        for folder in folders:
            for position in ['pre', 'post']:
                if position in rules[folder] and len(rules[folder][position]) > 0:
                    if position == 'pre':
                        post_rules = rules[folder].get('post', [])
                        rules[folder]['post'] = [post_rule for post_rule in post_rules if
                                                 post_rule['id'] not in [rule['id'] for rule in
                                                                         rules[folder][position]]]
                        # TODO Review logic for checking post rulebase duplicates, possibly remove if not necessary
                        # if position == 'post':
                        #     for rule in rules[folder][position]:
                        #         if 'pre' in rules[folder]:
                        #             for pre_rule in rules[folder]['post']:
                        #                 if rule['id'] == pre_rule['id']:
                        #                     rules[folder]['pre'].remove(pre_rule)
    except Exception as e:
        raise e

###############################################################
# Extract all available configuration from Prisma Access Tenant
###############################################################
@click.command()
@click.option('--folders', multiple=True, default=["Shared", "Service Connections",
                                                   "Remote Networks", "Mobile Users", "Mobile Users Explicit Proxy"])
@click.option('--filename', default='config.json')
def get_configuration(folders, filename):
    """

    Args:
        filename: Filename of the exported JSON configuration
        folders: Prisma Access Folders to utilize for queries
        session: SASE Authentication Token
    Returns:

    """
    session = create_session()
    excluded_objects = ["Application", "Certificate"]
    inspect_objects = [mobile, iam, objects, network, security, identity, subscription, tenancy]
    config = {'predefined': {}}

    def get_items(session, folder, key, obj):
        """Get the items from the API endpoint.

        Args:
            session (PanApiSession): The authenticated API session.
            folder (str): The folder to retrieve the items from.
            obj (object): The object that represents the endpoint.

        Returns:
            list: A list of items or "Not Found" if no items are found.
        """
        predefined = []
        shared = []

        def unpack_items(items, rule=False, sc=False, ba=False, mu=False):
            """Unpack the items from the API response.

            Args:
                items (list): The list of items to unpack.

            Returns:
                list: A list of unpacked items.
            """
            if items is not None:
                unpacked = []
                for item in items:
                    logger.debug(f'Checking if {item} has a payload attribute')
                    if hasattr(item, "payload"):
                        if hasattr(item, "_headers"):
                            delattr(item, '_headers')
                        logger.debug(f'Checking if {item} has a folder attribute')
                        if hasattr(item, 'folder'):
                            logger.debug(f'Checking if {item} folder is predefined')
                            if item.folder in ["All", "Prisma Access", "predefined"]:
                                logger.debug(f'Determined {item} is predefined because {item.folder} matches')
                                if rule:
                                    logger.debug(
                                        f'Determined {item} is predefined default rule because {item.folder} matches')
                                else:
                                    predefined.append(item.payload)
                            elif item.folder == 'Shared':
                                logger.debug(f'Determined {item} is shared because {item.folder} matches')
                                shared.append(item.payload)
                            else:
                                logger.debug(f'Determined {item} matches folder {folder}')
                                unpacked.append(item.payload)
                        else:
                            logger.debug(f'Determined {item} does not have a folder')
                            unpacked.append(item.payload)
                            if sc:
                                return {'Service Connections': unpacked}
                            elif ba:
                                return {'Remote Networks': unpacked}
                            elif mu:
                                return {'Mobile Users': unpacked}
                            else:
                                logger.debug(f'Returning list of items for {items} that ARE Shared')
                                return {'Shared': unpacked}
                if len(unpacked) > 0:
                    logger.debug(f'Returning list of items for {items} that are NOT predefined')
                    return {folder: unpacked}
                if len(predefined) > 0:
                    logger.debug(f'Returning list of items for {items} that ARE predefined')
                    return {'predefined': predefined}
                if len(shared) > 0:
                    logger.debug(f'Returning list of items for {items} that ARE Shared')
                    return {'Shared': shared}

        if hasattr(obj, '_position'):
            unpacked_dict = {}
            for idx, position in enumerate(obj._position):
                logger.debug(f'Iterating for {key} at position: {position} in folder: {folder}')
                items = obj(folder=folder, position=position)
                item_list = items.list(session)
                if item_list is not None:
                    logger.debug(f'Unpacking items for {key} at position: {position}')
                    unpacked = unpack_items(item_list, rule=True)
                    logger.debug(f'Unpacked items for {key} at position: {position}')
                    if folder == list(unpacked.keys())[0]:
                        if folder in unpacked_dict:
                            unpacked_dict[folder][position] = unpacked[folder]
                        else:
                            unpacked_dict[folder] = {position: unpacked[folder]}
                else:
                    logger.debug(f'Nothing to retrieve for {key} at position: {position}')
            return unpacked_dict
        if hasattr(obj, '_no_folder'):
            items = obj(no_folder=True)
            item_list = items.list(session)
            if item_list is not None:
                unpacked = unpack_items(item_list)
                return unpacked
            else:
                logger.debug(f'Nothing to retrieve for {key} object passed with no folder')
                return "Not Found"
        else:
            mu_pinning = ["global_settings", "infrastructure_settings", "locations"]
            items = obj(folder=folder)
            item_list = items.list(session)
            if item_list is not None:
                if key == "service_connections":
                    unpacked = unpack_items(item_list, sc=True)
                    return unpacked
                elif key == "remote_networks":
                    unpacked = unpack_items(item_list, ba=True)
                    return unpacked
                elif key in mu_pinning:
                    unpacked = unpack_items(item_list, mu=True)
                    return unpacked
                else:
                    unpacked = unpack_items(item_list)
                    return unpacked
            else:
                logger.debug(f'Nothing to retrieve for {key} object passed')
                return "Not Found"

    def match_folder(folder, items={}):
        if items:
            if folder in items:
                if len(items[folder]) > 0:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    try:
        for folder in folders:
            logger.info(f'Updating configuration for folder: {folder}')
            config.update({folder: {}})
            for inspected_obj in inspect_objects:
                section = str(inspected_obj.__name__).split('panapi.config.')[1]
                config[folder].update({section: {}})
                if section not in config['predefined']:
                    config['predefined'].update({section: {}})
                for name, obj in inspect.getmembers(inspected_obj):
                    if name in excluded_objects:
                        # SKIP Endpoint
                        continue
                    else:
                        if hasattr(obj, '_endpoint'):
                            endpoint = str(obj._endpoint)
                            logger.info(f'Acquired endpoint: {endpoint}')
                            key_name = (endpoint.rsplit("/", 1)[1]).replace("-", "_")
                            if hasattr(obj, '_required'):
                                if folder in obj._required:
                                    logger.info(f'Getting required items for: {key_name} for folder: {folder}')
                                    items = get_items(session, folder, key_name, obj)
                                    if match_folder(folder, items):
                                        config[folder][section].update({key_name: items[folder]})
                                    elif match_folder('predefined', items):
                                        if key_name not in config['predefined'][section]:
                                            config['predefined'][section].update({key_name: items['predefined']})
                                        else:
                                            continue
                                    elif match_folder('Shared', items):
                                        if key_name not in config['Shared'][section] and items is not None:
                                            config['Shared'][section].update({key_name: items['Shared']})
                                        else:
                                            continue
                                    else:
                                        continue
                            else:
                                logger.info(f'Getting non required items for: {key_name}')
                                items = get_items(session, folder, key_name, obj)
                                if match_folder(folder, items):
                                    config[folder][section].update({key_name: items[folder]})
                                else:
                                    if match_folder('predefined', items):
                                        if key_name not in config['predefined'][section]:
                                            config['predefined'][section].update({key_name: items['predefined']})
                                        else:
                                            continue
        # Remove empty keys
        empty_keys = [k for k, v in config.items() if not v]
        for k in empty_keys:
            logger.debug(f'Removing empty key: {k}')
            del config[k]
        # Cleanup empty dicts
        config = {key: {inner_key: inner_value for inner_key, inner_value in value.items()
                        if bool(inner_value)} for key, value in config.items()}
        # return config
        generate_json_file(filename, config)

    except Exception as e:
        logger.critical(f'Failed to acquire configuration with error: {e}')
        print(e)


###############################
# Generates a JSON file output.
###############################
def generate_json_file(filename, rules):
    """
        Args:
            filename: the actual filename to generate for json
            rules: Dictionary of rules generated from the get_rules() function
    """
    try:
        with open(filename, 'w') as f:
            # Convert dictionary to JSON
            json.dump(rules, f, indent=4)
    except Exception as e:
        raise e


###############################
# Generates a CSV file output.
###############################
def generate_csv_rules(folders, rules_dict, type, suffix):
    """

    Args:
        suffix: Append string suffix to csv file
        folders: List of Prisma Access folders to cycle through
        rules_dict: Dictionary of rules generated from the get_rules() function
        type: # Str value for the rule type to modify csv filename

    Returns:

    """
    try:
        for folder in folders:
            for position in ['pre', 'post']:
                if position in rules_dict[folder]:
                    if len(rules_dict[folder][position]) > 0:
                        folder_data = rules_dict[folder][position]
                        new_csv = open(f'{folder.lower()}_{type.lower()}_{position}_{suffix}.csv',
                                       'w', newline='', encoding='utf-8')
                        csv_writer = csv.writer(new_csv)
                        count = 0

                        for item in folder_data:
                            if count == 0:
                                # Writing headers of CSV file
                                header = item.keys()
                                csv_writer.writerow(header)
                                count += 1

                            # Writing data of CSV file
                            csv_writer.writerow(item.values())
                        new_csv.close()
    except Exception as e:
        raise e


def cleanup():
    os.kill(os.getpid(), signal.SIGINT)


if __name__ == '__main__':
    try:
        get_configuration()
        atexit.register(cleanup)
    except Exception as e:
        print(e)
        sys.exit(1)
