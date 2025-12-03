import logging
from pathlib import Path

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.config import get_settings
from app.zoho_client import zoho_client
from app.url_builder import build_redirect_url, determine_tier, get_fallback_url

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Zoho Score Router",
    description="Routes users based on their Zoho CRM score",
    version="1.0.0",
)

# Templates directory
templates_dir = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))


@app.get("/", response_class=HTMLResponse)
async def route_by_score(
    request: Request,
    key: str = Query(..., description="Key to look up in Zoho CRM"),
):
    """Show loading page that polls for score."""
    logger.info("=== INCOMING REQUEST ===")
    logger.info(f"URL: {request.url}")
    logger.info(f"Method: {request.method}")
    logger.info(f"Client: {request.client}")
    logger.info(f"Headers:")
    for name, value in request.headers.items():
        logger.info(f"  {name}: {value}")

    return templates.TemplateResponse("loading.html", {"request": request, "key": key})


@app.get("/check-score", response_class=JSONResponse)
async def check_score(
    key: str = Query(..., description="Key to look up in Zoho CRM"),
):
    """Polling endpoint to check if score is available and return personalized redirect URL."""
    settings = get_settings()
    fallback_url = get_fallback_url()

    try:
        lead_data = await zoho_client.get_routing_data_for_key(key)

        if lead_data is not None:
            # Determine tier and build redirect URL
            tier = determine_tier(
                lead_data.score,
                settings.sql_threshold,
                settings.sal_threshold,
            )
            redirect_url = build_redirect_url(lead_data, tier)

            logger.info(
                f"Routing decision for {key}: "
                f"score={lead_data.score}, tier={tier.value}, "
                f"vsl_source={lead_data.vsl_source}, redirect={redirect_url}"
            )

            return {"status": "ready", "redirect_url": redirect_url}

        # Score not found yet - keep polling
        logger.info(f"Score not found for {key}, client should keep polling")
        return {"status": "not_found", "redirect_url": fallback_url}

    except Exception as e:
        logger.error(f"Error checking score for {key}: {e}")
        return {"status": "error", "redirect_url": fallback_url}


@app.get("/health")
async def health_check():
    """Health check endpoint for Railway and load balancers."""
    return {"status": "healthy"}
