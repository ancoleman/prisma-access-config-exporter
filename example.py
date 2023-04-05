import config_exporter
import logging

folders = ['Shared', 'Remote Networks', 'Mobile Users', 'Mobile Users Explicit Proxy']

#################
# Setup Logging
#################
logger = config_exporter.setup_logger('config_logger', 'config_exporter.log', file_level=logging.DEBUG,
                                      stream_level=logging.INFO)
config_exporter.logger = logger

#################
# Session
#################
session = config_exporter.create_session()

#################
# Generate Config
#################
config = config_exporter.get_configuration(session, folders)
config_exporter.generate_json_file('config.json', config)
