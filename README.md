# prisma-access-rule-exporter


[![license](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE) [![support](https://img.shields.io/badge/Support%20Level-Community-yellowgreen)](./SUPPORT.md)

## Description
Simple Export Script to Palo Alto Networks SASE Tenant Configuration to JSON file output.
Additionally, the utility can export all folder rulebases into CSV.

### Requirements
* Python 3.9+
* OAUTH Service Account Credentials file

### Currently Tested and Supported Configuration Output Items
* Identity
  * authentication_profiles
  * local_users
  * saml_server_profiles
* Network
  * bandwidth_allocations
  * internal_dns_servers
  * shared_infrastructure_settings
  * ike_crypto_profiles
  * ike_gateways
  * ipsec_crypto_profiles
  * ipsec_tunnels
  * qos_profiles
  * remote_networks
* Objects
  * address_groups
  * addresses
  * application_groups
  * applications
  * app_override_rules
  * auto_tag_actions
  * certificate_profiles
  * schedules
  * services
  * service_groups
  * dynamic_user_groups
  * tags
* Security
  * anti_spyware_profiles
  * dns_security_profiles
  * decryption_profiles
  * file_blocking_profiles
  * profile_groups
  * url_access_profiles
  * url_categories
  * vulnerability_protection_profiles
  * vulnerability_protection_signatures
  * wildfire_anti_virus_profiles
  * decryption_exclusions
  * security_rules
  * decryption_rules
* Subscription
  * instances
  * licenses

#### Example Credentials config.yaml
Create the config.yaml file in the root directory.
```yaml
---
scope: profile tsg_id:YOURTENANTID email
client_id: SA@YOURID.iam.panserviceaccount.com
client_secret: YOURSECRET
grant_type: client_credentials
token_url: https://auth.apps.paloaltonetworks.com/am/oauth2/access_token
```

### Example Usage
Currently, no CLI has been added to this project, so all parameters need to be added to the script.

#### Paramters
* folders = ['Shared', 'Remote Networks', 'Mobile Users', 'Mobile Users Explicit Proxy']

```
git clone https://github.com/ancoleman/prisma-access-rule-exporter
cd prisma-access-rule-exporter
pip install -r requirements.txt
```

```python
#Example from example.py
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
```


## Version History


* 0.1
    * Initial Release

## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details