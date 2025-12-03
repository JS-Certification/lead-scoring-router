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
    zoho_score_field: str = "Score_Number_V2"
    zoho_key_field: str = "Zoho_Form_Submission_ID"
    zoho_vsl_source_field: str = "VSL_Source"

    # Score tier thresholds
    # SQL: score > sql_threshold (qualified for campaign-specific booking)
    # SAL: score >= sal_threshold (middle tier, generic booking)
    # UNQ: score < sal_threshold (unqualified, thank you page)
    sql_threshold: float = 75.0
    sal_threshold: float = 50.0

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
