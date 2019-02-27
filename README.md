# Python helper class for reading secrets from Azure Key Vault

The ```KeyVaultSettings``` class provides a simple way to initialize an object that contains all of the secrets from an Azure Key Vault as properties. That object can then be passed around to methods and functions within your code that need access to those secrets.

For a detailed walk-through of how to set up a key vault, store secrets, and configure programmatic access to those secrets, see the blog post [Storing secrets in Azure Key Vault](https://www.dougmahugh.com/azure-key-vault/).

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

Note the required packages in [requirements.txt](https://github.com/dmahugh/azure-key-vault/blob/master/requirements.txt), which install the Python client library for Azure Key Vault.
