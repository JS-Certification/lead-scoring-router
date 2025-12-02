import httpx
import time
import logging
from typing import Any

from app.config import get_settings

logger = logging.getLogger(__name__)


class ZohoClient:
    """Client for interacting with Zoho CRM API."""

    def __init__(self):
        self._access_token: str | None = None
        self._token_expiry: float = 0

    async def _refresh_access_token(self) -> str:
        """Exchange refresh token for a new access token."""
        settings = get_settings()

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.zoho_accounts_url}/oauth/v2/token",
                data={
                    "refresh_token": settings.zoho_refresh_token,
                    "client_id": settings.zoho_client_id,
                    "client_secret": settings.zoho_client_secret,
                    "grant_type": "refresh_token",
                },
            )
            response.raise_for_status()
            data = response.json()

        self._access_token = data["access_token"]
        # Token expires in ~1 hour, refresh 5 minutes early
        expires_in = data.get("expires_in", 3600)
        self._token_expiry = time.time() + expires_in - 300

        logger.info("Zoho access token refreshed successfully")
        return self._access_token

    async def get_access_token(self) -> str:
        """Get a valid access token, refreshing if necessary."""
        if self._access_token is None or time.time() >= self._token_expiry:
            return await self._refresh_access_token()
        return self._access_token

    async def search_record_by_key(self, key: str) -> dict[str, Any] | None:
        """
        Search for a record in the configured module by key field.

        Returns the first matching record or None if not found.
        """
        settings = get_settings()
        access_token = await self.get_access_token()

        url = f"{settings.zoho_api_domain}/crm/v8/{settings.zoho_module_name}/search"
        headers = {"Authorization": f"Zoho-oauthtoken {access_token}"}
        params = {"criteria": f"({settings.zoho_key_field}:equals:{key})"}

        # Log the full request
        logger.info(f"=== ZOHO API REQUEST ===")
        logger.info(f"GET {url}")
        logger.info(f"Params: {params}")
        logger.info(f"Headers: Authorization: Zoho-oauthtoken {access_token[:20]}...")

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=headers)

            # Log the full response
            logger.info(f"=== ZOHO API RESPONSE ===")
            logger.info(f"Status: {response.status_code}")
            logger.info(f"Body: {response.text}")

            if response.status_code == 204:
                # No records found
                logger.info(f"No record found for key: {key}")
                return None

            if response.status_code == 200:
                data = response.json()
                records = data.get("data", [])
                if records:
                    logger.info(f"Found record for key: {key}")
                    return records[0]
                return None

            # Log unexpected responses
            logger.warning(
                f"Unexpected response from Zoho: {response.status_code} - {response.text}"
            )
            response.raise_for_status()

        return None

    async def get_score_for_key(self, key: str) -> float | None:
        """
        Get the score for a record identified by key.

        Returns the score value or None if record not found or score field is empty.
        """
        settings = get_settings()
        record = await self.search_record_by_key(key)

        if record is None:
            return None

        score = record.get(settings.zoho_score_field)

        if score is None:
            logger.info(f"Score field '{settings.zoho_score_field}' not found or empty")
            return None

        try:
            return float(score)
        except (ValueError, TypeError):
            logger.warning(f"Could not convert score to float: {score}")
            return None


# Singleton instance
zoho_client = ZohoClient()
