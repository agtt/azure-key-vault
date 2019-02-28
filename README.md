# Python helper class for reading secrets from Azure Key Vault

The ```KeyVaultSettings``` class provides a simple way to initialize an object that contains all of the secrets from an Azure Key Vault as properties. That object can then be passed around to methods and functions within your code that need access to those secrets.

The key vault secrets are read when a class instance is created. You can add new settings to the key vault at any time (through the Azure Portal, Azure CLI, or programmatically), and they'll automatically show up as properties of ```KeyVaultSettings``` the next time it is instantiated.

# Installation
KeyVaultSettings uses the Azure Key Vault client library for Python, and the prerequisites are in this repo's [requirements.txt](https://github.com/dmahugh/azure-key-vault/blob/master/requirements.txt) file. To install:

* Clone this repo
* Install Python (version 3.6 or higher)
* In the root folder of the cloned repo, install the prerequisites with the command ```python -m pip install -r requirements.txt```

# Usage
Four settings are needed to initialize a KeyVaultSettings instance:

* Client ID (App ID), App Secret (Password), and Tenant ID for an identity that has Get and List permissions for the key vault (typically a service principal identity)
* Key Vault URI for the key vault (which you can find under _DNS Name_ in the Azure Portal)

Those settings can be read from a JSON file, or can be passed to the constructor as keyword arguments. Here's a simple example of how to use AzureKeyVault:

```python
from akvheler import KeyVaultSettings

settings = KeyVaultSettings(client_id="YOUR_CLIENT_ID",
                            app_secret="YOUR_APP_SECRET",
                            tenant_id="YOUR_TENANT_ID",
                            key_vault_uri="https://YOUR_VAULT_NAME.vault.azure.net/")

print(f"The MY_SECRET setting is {settings.MY_SECRET}")
```

Here's an example of the str/repr representation of a typical KeyVaultSettings instance in one of my apps:

```
<class 'akvhelper.KeyVaultSettings'> <vault: https://MY_VAULT_NAME.azure.net/> <settings: db_database, db_password, db_schema, db_server, db_username, gh_token, gh_username, so_client_id, so_key, vsts_org_url, vsts_token>
```
For a detailed walk-through of how to set up a key vault, store secrets, and configure programmatic access to those secrets, see the blog post [Storing secrets in Azure Key Vault](https://www.dougmahugh.com/azure-key-vault/).

# Contributing
This project is a work in progress, and pull requests, feature requests and issues are welcome. I've implemented the functionality I needed for various projects, but I'm interested in knowing what may be useful to others, so please [log an issue](https://github.com/dmahugh/azure-key-vault/issues) if you have a suggestion. Thanks!

# License
This project is licensed under the [MIT License](https://github.com/dmahugh/azure-key-vault/blob/master/LICENSE).


