"""URL building utilities for personalized score-based routing."""

from urllib.parse import urlencode, urljoin
from enum import Enum

from app.utm_mappings import (
    BASE_URL,
    DEFAULT_SQL_PATH,
    SAL_DEFAULT_PATH,
    SAL_FAQ_PATH,
    UNQ_PATH,
    UTM_TO_URL,
)
from app.zoho_client import LeadRoutingData


class ScoreTier(Enum):
    """Score tiers for lead routing."""

    SQL = "sql"  # score > 64 - Sales Qualified Lead
    SAL = "sal"  # 49 <= score <= 64 - Sales Accepted Lead
    UNQ = "unq"  # score < 49 - Unqualified


def determine_tier(score: float, sql_threshold: float, sal_threshold: float) -> ScoreTier:
    """
    Determine which tier a score falls into.

    Args:
        score: The lead's score
        sql_threshold: Score must be > this for SQL tier
        sal_threshold: Score must be >= this for SAL tier

    Returns:
        ScoreTier enum value
    """
    if score > sql_threshold:
        return ScoreTier.SQL
    elif score >= sal_threshold:
        return ScoreTier.SAL
    else:
        return ScoreTier.UNQ


def build_personalization_params(lead_data: LeadRoutingData) -> dict[str, str]:
    """
    Build query parameters for URL personalization.

    Only includes params for non-empty fields.
    """
    params = {}

    if lead_data.first_name:
        params["name"] = lead_data.first_name
    if lead_data.last_name:
        params["last name"] = lead_data.last_name  # Space in key as per requirement
    if lead_data.email:
        params["email"] = lead_data.email

    return params


def get_sql_path(vsl_source: str | None) -> str:
    """
    Get booking page path for SQL tier based on vsl_source.

    Falls back to default if vsl_source not found in mapping.
    """
    if vsl_source and vsl_source in UTM_TO_URL:
        return UTM_TO_URL[vsl_source]
    return DEFAULT_SQL_PATH


def get_sal_path(vsl_source: str | None) -> str:
    """
    Get booking page path for SAL tier based on vsl_source.

    Uses FAQ path if "-faq-" is in the vsl_source, otherwise default SAL path.
    """
    if vsl_source and "-faq-" in vsl_source:
        return SAL_FAQ_PATH
    return SAL_DEFAULT_PATH


def build_redirect_url(lead_data: LeadRoutingData, tier: ScoreTier) -> str:
    """
    Build the complete redirect URL for a lead based on their tier.

    SQL & SAL tiers get personalized URLs with query params.
    UNQ tier gets the thank you page (no personalization).

    Args:
        lead_data: The lead's routing data from Zoho
        tier: The determined score tier

    Returns:
        Complete redirect URL with path and query params
    """
    # Determine the path based on tier
    if tier == ScoreTier.SQL:
        path = get_sql_path(lead_data.vsl_source)
    elif tier == ScoreTier.SAL:
        path = get_sal_path(lead_data.vsl_source)
    else:  # UNQ
        # UNQ tier: No personalization, just thank you page
        return urljoin(BASE_URL, UNQ_PATH)

    # Build full URL with personalization for SQL/SAL
    base = urljoin(BASE_URL, path)
    params = build_personalization_params(lead_data)

    if params:
        # urlencode handles proper encoding including "last name" -> "last%20name"
        query_string = urlencode(params)
        return f"{base}?{query_string}"

    return base


def get_fallback_url() -> str:
    """Get the fallback URL for errors/timeouts (thank you page)."""
    return urljoin(BASE_URL, UNQ_PATH)
