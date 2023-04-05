import panapi
from panapi.config import \
    iam, \
    security, \
    identity, \
    objects, \
    network, \
    subscription, \
    mobile
import inspect
import time
import json
import logging
import csv

__author__ = "Palo Alto Networks"
__copyright__ = "Copyright 2023, Palo Alto Networks"
__credits__ = ["Robert Hagen", "Anton Coleman"]
__license__ = "MIT"
__version__ = ".1"
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


logger = ""


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


def get_rules(session, folders, rule_type='security'):
    """

    Args:
        session: Session object from create_session() function
        folders: List of Prisma Access folders to cycle through
        rule_type: security, decrypt, auth

    Returns:

    """
    # Stages Empty Dictionary for Rules
    rules_config = {}
    # Loops through each folder
    for folder in folders:
        # Creates a nested dict for folder in rules_config
        rules_config.update({folder: {}})
        # Loop through the rulebase positioning
        for position in ['pre', 'post']:
            if rule_type == 'security':
                rules = security.SecurityRule(
                    folder=folder,
                    position=position
                )
            if rule_type == 'auth':
                rules = identity.AuthenticationRule(
                    folder=folder,
                    position=position
                )
            if rule_type == 'decrypt':
                rules = security.DecryptionRule(
                    folder=folder,
                    position=position
                )
            response = rules.list(session)
            # If the response was none, nothing is populated in the dict for that folder or position
            if response is not None:
                # Check if the response has items in a list or if the list is empty
                if len(response) > 0:
                    # Stage an empty list to hold object payload values
                    rules_list = []
                    for rule in response:
                        # Check if the rule is actually contained in that specified folder, or in shared.
                        if rule.folder == folder:
                            # Cleanup from the output, _headers attribute is of no value for parsing
                            delattr(rule, '_headers')
                            # Add rule to the rules list
                            rules_list.append(rule.payload)
                    # Add all rules for folder and position to the dictionary
                    rules_config[folder].update({position: rules_list})
    return rules_config


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


def get_configuration(session, folders):
    """

    Args:
        product_type: RN or MU
        time_period: 30d, 90d, 365d
    Returns:

    """
    excluded_objects = ["Application", "Certificate"]
    inspect_objects = [mobile, iam, objects, network, security, identity, subscription]
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

        def unpack_items(items):
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
                            if item.folder == 'predefined':
                                logger.debug(f'Determined {item} is predefined')
                                predefined.append(item.payload)
                            elif item.folder == 'Shared':
                                logger.debug(f'Determined {item} is shared')
                                shared.append(item.payload)
                            else:
                                logger.debug(f'Determined {item} matches folder {folder}')
                                unpacked.append(item.payload)
                        else:
                            logger.debug(f'Determined {item} does not have a folder')
                            unpacked.append(item.payload)
                            logger.info(f'Returning list of items for {items} that ARE Shared')
                            return {'Shared': unpacked}
                if len(unpacked) > 0:
                    logger.info(f'Returning list of items for {items} that are NOT predefined')
                    return {folder: unpacked}
                if len(predefined) > 0:
                    logger.info(f'Returning list of items for {items} that ARE predefined')
                    return {'predefined': predefined}
                if len(shared) > 0:
                    logger.info(f'Returning list of items for {items} that ARE Shared')
                    return {'Shared': shared}

        if hasattr(obj, '_position'):
            for position in obj._position:
                logger.info(f'Iterating for {key} at position: {position} in folder: {folder}')
                items = obj(folder=folder, position=position)
                item_list = items.list(session)
                if item_list is not None:
                    logger.warn(f'Unpacking items for {key} at position: {position}')
                    unpacked = unpack_items(item_list)
                    logger.warn(f'Unpacked items for {key} at position: {position}')
                    # unpacked = {folder: {position: unpacked[folder]}}
                else:
                    logger.warn(f'Nothing to retrieve for {key} at position: {position}')
                    unpacked = "Not Found"
            return unpacked
        elif hasattr(obj, '_no_folder'):
            items = obj(no_folder=True)
            item_list = items.list(session)
            if item_list is not None:
                unpacked = unpack_items(item_list)
                return unpacked
            else:
                logger.warn(f'Nothing to retrieve for {key} object passed with no folder')
                return "Not Found"
        else:
            items = obj(folder=folder)
            item_list = items.list(session)
            if item_list is not None:
                unpacked = unpack_items(item_list)
                return unpacked
            else:
                logger.warn(f'Nothing to retrieve for {key} object passed')
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
                                    else:
                                        if match_folder('predefined', items):
                                            if key_name not in config['predefined'][section]:
                                                config['predefined'][section].update({key_name: items['predefined']})
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
        return config

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
