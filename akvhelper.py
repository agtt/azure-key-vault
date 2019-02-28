"""helper functions for cf_crawler
"""
import json

from azure.common.credentials import ServicePrincipalCredentials
from azure.keyvault import KeyVaultClient
from azure.keyvault.v7_0.models.key_vault_error_py3 import KeyVaultErrorException


class KeyVaultSettings:
    """
    Settings object, contains settings from Azure Key Vault as self. properties.
    """

    def __init__(self, **kwargs):
        """Initialize instance, set properties from Azure Key Vault secrets.
        All secrets in the Key Vault are stored in the instance.

        Access to an Azure Key Vault requires these auth settings:
        client_id, app_secret, tenant_id, key_vault_uri.

        To read those values from a JSON file, use this constructor syntax:
        KeyVaultSettings(filename="filename.json")

        Alternatively, you can explicitly specify the auth settings as
        keyword arguments like this:
        KeyVaultSettings(client_id="value", app_secret="value",
                         tenant_id="value", key_vault_uri="value")
        """

        # Initialize the config settings used for access to the key vault.
        self._config = {
            "client_id": "",
            "app_secret": "",
            "tenant_id": "",
            "key_vault_uri": "",
        }

        keywords = {_ for _ in kwargs}
        if keywords == set(["filename"]):
            # read Key Vault access credentials from private JSON file
            with open("../_private/keyvault-cft-vault.json") as settings_file:
                settings = json.load(settings_file)
            for setting in self._config:
                self._config[setting] = settings[setting]
        elif keywords == set(["client_id", "app_secret", "tenant_id", "key_vault_uri"]):
            # Key Vault access credentials passed as keyword arguments
            for setting in self._config:
                self._config[setting] = kwargs[setting]
        else:
            raise SyntaxError("Invalid constructor syntax for KeyVaultSetting class.")

        # Get all secrets from Azure Key Vault and store them as self. properties.
        # We first get the list of all secrets in the vault, then get the values.
        secret_metadata = self.get_secrets()
        secret_names = [
            secret_item.id.split("/")[-1] for secret_item in secret_metadata
        ]
        secrets = self.get_secret_values(secret_names)
        for secret_name in secret_names:
            self.__dict__[secret_name.replace("-", "_")] = secrets[secret_name]

    def __repr__(self):
        """Represent an instance of this class as a string.
        This is for debugging convenience, not intended for eval() useage.
        """
        properties = sorted(
            [prop_name for prop_name in self.__dict__ if not prop_name == "_config"]
        )
        return (
            f"{self.__class__} "
            f"<vault: {self._config['key_vault_uri']}> "
            f"<settings: {', '.join(properties)}>"
        )

    def get_secret(self, secret_name):
        """Get a secret from Key Vault.
        """
        credentials = ServicePrincipalCredentials(
            client_id=self._config["client_id"],
            secret=self._config["app_secret"],
            tenant=self._config["tenant_id"],
        )
        client = KeyVaultClient(credentials)

        try:
            secret_bundle = client.get_secret(
                self._config["key_vault_uri"], secret_name, ""
            )
            secret_value = secret_bundle.value
        except KeyVaultErrorException:
            secret_value = ""

        return secret_value

    def get_secret_values(self, secret_names):
        """Get a list of secrets from Key Vault. Returns a dictionary.
        """
        credentials = ServicePrincipalCredentials(
            client_id=self._config["client_id"],
            secret=self._config["app_secret"],
            tenant=self._config["tenant_id"],
        )
        client = KeyVaultClient(credentials)

        secret_values = {}
        for secret_name in secret_names:
            try:
                secret_bundle = client.get_secret(
                    self._config["key_vault_uri"], secret_name, ""
                )
                secret_values[secret_name] = secret_bundle.value
            except KeyVaultErrorException:
                secret_values[secret_name] = ""

        return secret_values

    def get_secrets(self):
        """Get all of the secrets from Key Vault. Requires List permission.
        Returns a list of SecretItem objects as documented here:
        https://docs.microsoft.com/en-us/python/api/azure-keyvault/azure.keyvault.v7_0.models.secret_item_py3.secretitem?view=azure-python
        """
        credentials = ServicePrincipalCredentials(
            client_id=self._config["client_id"],
            secret=self._config["app_secret"],
            tenant=self._config["tenant_id"],
        )
        client = KeyVaultClient(credentials)

        try:
            secrets = client.get_secrets(self._config["key_vault_uri"])
        except KeyVaultErrorException:
            secrets = []

        return secrets
