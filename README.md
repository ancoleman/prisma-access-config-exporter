# prisma-access-config-exporter


[![license](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE) [![support](https://img.shields.io/badge/Support%20Level-Community-yellowgreen)](./SUPPORT.md)

## Description
Simple Export Script for Palo Alto Networks SASE Tenant Configuration to JSON file output.
Additionally, the utility can export all folder rulebases into CSV.


### Use Cases
* Exporting configuration
  * For auditing purposes 
  * For moving configuration between different CSP accounts
  * Generating Documentation
* What it is NOT used for:
  * Exporting configuration for backup purposes
  * Exporting configuration for disaster recovery purposes


### Requirements
* Docker Desktop 4.19+
* OAUTH Service Account Credentials file

### Currently Tested and Supported Configuration Output Items
* IAM
  * access_policies
  * permissions
  * roles
  * service_accounts
* Identity
  * authentication_profiles
  * local_users
  * saml_server_profiles
* Mobile
  * agent_profiles
  * authentication_settings
  * tunnel_profiles
  * global_settings
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

#### How to get OAUTH Service Account Credentials
1. Login to https://apps.paloaltonetworks.com
2. Click on the "Common Services" tab in the top navigation bar and select "Identity and Access"
3. Choose the tenant you want to export the configuration from
4. Click the "add" button in the top right corner of the dialog box
5. Select Identity Type and choose "Service Account" and provide the necessary information and then click "next"
6. Download the CSV credentials file, follow the below example to create the config.yaml file with the credentials
7. Click next and Assign Roles, Choose "All Apps and Services" with the role of "Auditor". Click "submit"

**NOTE:** The service account will need to be assigned at minimum "Auditor" role to be able to export the configuration.
You can assign it more permissive roles, but it's not required for the export.

#### Example Credentials config.yaml
Create the config.yaml **root** project directory. This file will be mounted to a docker container as a volume. If you update the file, it will be updated in realtime on the container.
```yaml
---
scope: profile tsg_id:YOURTENANTID email
client_id: SA@YOURID.iam.panserviceaccount.com
client_secret: YOURSECRET
grant_type: client_credentials
token_url: https://auth.apps.paloaltonetworks.com/am/oauth2/access_token
```

### Example Usage
A CLI has been added to this project, all CLI arguments have defaults set, however you can override those if you so choose. The cli commands are passed through using **docker compose run**.

#### CLI Options

| Option     | Default                                                                               |
|------------|---------------------------------------------------------------------------------------|
| --folders  | "Shared,Service Connections,Remote Networks,Mobile Users,Mobile Users Explicit Proxy" |
| --filename | "config.json"                                                                         |

```bash
git clone https://github.com/ancoleman/prisma-access-config-exporter
cd prisma-access-config-exporter
docker compose build
docker compose run pa_export
```

If you want to use the CLI options here is an example:
```bash
docker compose run pa_export --filename=customer1.json --folders="Shared,Mobile Users"
```

Files will be generated in:
* resources/config - The JSON configuration file will be stored here.
* resources/log - The audit/debug logs will be stored here.

## Version History


* 0.1
  * Initial Release
* 0.2
  * Introduce CLI, additional bug fixes
* 0.3
  * Package CLI with docker compose

## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details