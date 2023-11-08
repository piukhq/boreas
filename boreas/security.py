"""Security module for Boreas API."""

from __future__ import annotations

from functools import cache

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from fastapi import Security
from fastapi.security import APIKeyHeader
from tenacity import retry, stop_after_attempt, wait_exponential

from boreas.exceptions import InvalidTokenError
from boreas.settings import settings

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=3, max=12), reraise=True)
@cache
def load_secrets(secret_name: str) -> str:
    """Load secrets from Azure Key Vault."""
    kv_credential = DefaultAzureCredential()
    kv_client = SecretClient(vault_url=settings.keyvault_uri, credential=kv_credential)
    return kv_client.get_secret(secret_name).value


async def get_api_key(retailer_id: str, api_key_header: str = Security(api_key_header)) -> str | InvalidTokenError:
    """Check the API Key in the request header matches the one in Azure Key Vault."""
    if api_key_header == load_secrets(f"{retailer_id}-transactions-api-key"):
        return api_key_header
    raise InvalidTokenError
