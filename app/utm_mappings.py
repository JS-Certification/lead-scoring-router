"""UTM source to booking page URL mappings for score-based routing."""

# Base URL for all booking pages
BASE_URL = "https://pages.jayshettycoaching.com"

# SQL tier: Default booking page when vsl_source not found in mapping
DEFAULT_SQL_PATH = "/app-booking-jscs-website/"

# SAL tier paths
SAL_DEFAULT_PATH = "/app-booking-m/"
SAL_FAQ_PATH = "/app-booking-faq-m/"

# UNQ tier path
UNQ_PATH = "/u-application-ty/"

# Mapping from Zoho vsl_source field value to booking page path
# For SQL tier leads (score > 64), the vsl_source determines which booking page
UTM_TO_URL: dict[str, str] = {
    "booking-webinar": "/app-booking-webinar/",
    "booking-promo-be": "/app-booking-promo-be/",
    "booking-a": "/app-booking-a/",
    "booking-jscs-website": "/app-booking-jscs-website/",
    "booking-brochure": "/app-booking-brochure/",
    "booking-rnc-li": "/app-booking-rnc-li/",
    "booking-rnc-yt": "/app-booking-rnc-yt/",
    "booking-pro-be": "/app-booking-pro-be/",
    "booking-pro-b": "/app-booking-pro-b/",
    "booking-rnc-be": "/app-booking-rnc-be/",
    "booking-rnc-a": "/app-booking-rnc-a/",
    "booking-rnc-a-yt": "/app-booking-rnc-yt/",
    "booking-rnc-bing": "/app-booking-rnc-a-bing/",
    "booking-rnc-f": "/app-booking-rnc-f/",
    "booking-rnc-s": "/app-booking-rnc-s/",
    "booking-rnc-b": "/app-booking-rnc-b/",
    "booking-amb-rnc": "/app-booking-amb/",
    "booking-rnc-g": "/app-booking-rnc-g/",
    "booking-rnc-misc": "/app-booking-misc/",
    "booking-c2c-be": "/app-booking-c2c-be/",
    "booking-c2c-a": "/app-booking-c2c-a/",
    "booking-c2c-a-yt": "/app-booking-c2c-yt/",
    "booking-c2c-f": "/app-booking-c2c-f/",
    "booking-c2c-s": "/app-booking-c2c-s/",
    "booking-c2c-b": "/app-booking-c2c-b/",
    "booking-amb-c2c": "/app-booking-amb/",
    "booking-c2c-misc": "/app-booking-misc/",
    "booking-ovsl-be": "/app-booking-ovsl-be/",
    "booking-ovsl-a": "/app-booking-ovsl-a/",
    "booking-ovsl-a-yt": "/app-booking-ovsl-yt/",
    "booking-ovsl-f": "/app-booking-ovsl-f/",
    "booking-ovsl-w": "/app-booking-ovsl-w/",
    "booking-ovsl-b": "/app-booking-ovsl-b/",
    "booking-ovsl-s": "/app-booking-ovsl-s/",
    "booking-ovsl-bing": "/app-booking-ovsl-a-bing/",
    "booking-ovsl-misc": "/app-booking-misc/",
    "booking-be": "/app-booking-be/",
    "booking-pathway": "/app-booking-pathway/",
    "booking-funnel": "/app-booking-funnel/",
    "booking-misc": "/app-booking-misc/",
    "booking-dyp-be": "/app-booking-dyp-be/",
    "booking-dyp-a": "/app-booking-dyp-a/",
    "booking-dyp-f": "/app-booking-dyp-f/",
    "booking-dyp-s": "/app-booking-dyp-s/",
    "booking-dyp-b": "/app-booking-dyp-b/",
    "booking-dyp-g": "/app-booking-dyp-g/",
    "booking-dyp-li": "/app-booking-dyp-li/",
    "booking-amb-dyp": "/app-booking-amb/",
    "booking-pro-a": "/app-booking-pro-a/",
    "booking-pro-f": "/app-booking-pro-f/",
    "booking-pro-s": "/app-booking-pro-s/",
    "booking-pro-g": "/app-booking-pro-g/",
    "booking-pro-li": "/app-booking-pro-li/",
    "booking-amb-pro": "/app-booking-amb/",
    "booking-faq-be": "/app-booking-faq-be/",
    "booking-faq-f": "/app-booking-faq-f/",
    "booking-faq-b": "/app-booking-faq-b/",
    "booking-dyp-a-fbig": "/app-booking-dyp-a-fbig/",
    "booking-fyf-b": "/app-booking-fyf-b/",
    "booking-fyf-be": "/app-booking-fyf-be/",
    "booking-fyf-a-fbig": "/app-booking-fyf-a-fbig/",
    "booking-fyf-a-yt": "/app-booking-fyf-a-yt/",
    "booking-fyf-f": "/app-booking-fyf-f/",
    "booking-faq-a-g": "/app-booking-faq-a-g/",
    "booking-c2c-a-g": "/app-booking-c2c-a-g/",
    "booking-faq-a-fbig": "/app-booking-faq-a-fbig/",
    "booking-fyf-s": "/app-booking-fyf-s/",
    "booking-fyf-a-g": "/app-booking-fyf-a-g/",
    "booking-c2c-a-g-ao": "/app-booking-c2c-a-g-ao/",
    "booking-c2c-a-fbig-ao": "/app-booking-c2c-a-fbig-ao/",
    "booking-ovsl-a-g-ao": "/app-booking-ovsl-a-g-ao/",
    "booking-ovsl-a-fbig-ao": "/app-booking-ovsl-a-fbig-ao/",
    "new-website": "/app-booking-jscs-website/",
    "booking-ovsl-a-fbig": "/app-booking-ovsl-a-fbig/",
    "booking-ycv-a-fbig": "/app-booking-ycv-a-fbig/",
    "booking-ycv-a-g": "/app-booking-ycv-a-g/",
    "booking-ycv-a-yt": "/app-booking-ycv-a-yt/",
    "booking-ycv-be": "/app-booking-ycv-be/",
    "booking-ycv-f": "/app-booking-ycv-f/",
}
