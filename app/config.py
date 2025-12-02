from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Zoho OAuth credentials
    zoho_client_id: str
    zoho_client_secret: str
    zoho_refresh_token: str

    # Zoho API endpoints
    zoho_api_domain: str = "https://www.zohoapis.com"
    zoho_accounts_url: str = "https://accounts.zoho.com"

    # Zoho CRM module configuration
    zoho_module_name: str = "Form_Submissions"
    zoho_score_field: str = "Score"
    zoho_key_field: str = "Email"

    # Score threshold for routing
    score_threshold: float = 70.0

    # Redirect URLs
    success_redirect_url: str  # e.g., Calendly link
    thank_you_page_url: str | None = None  # If None, use internal thank you page

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
