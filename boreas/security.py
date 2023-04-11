from functools import cache

from azure.core.exceptions import HttpResponseError
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from fastapi import Security
from fastapi.security import APIKeyHeader
from tenacity import retry, stop_after_attempt, wait_exponential

import boreas.settings as settings
from boreas.exceptions import InvalidTokenError

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=3, max=12),
    reraise=True,
)
@cache
def load_secrets(secret_name: str):
    if settings.keyvault_uri is None:
        raise Exception("Vault Error: settings.keyvault_uri not set")

    kv_credential = DefaultAzureCredential()
    kv_client = SecretClient(vault_url=settings.keyvault_uri, credential=kv_credential)

    try:
        return kv_client.get_secret(secret_name).value
    except HttpResponseError as e:
        raise Exception(f"Vault Error: {e}") from e


async def get_api_key(retailer_id: str, api_key_header: str = Security(api_key_header)):
    if api_key_header == load_secrets(f"{retailer_id}-transactions-api-key"):
        return api_key_header
    else:
        raise InvalidTokenError()
