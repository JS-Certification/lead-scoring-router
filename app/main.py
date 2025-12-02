import logging
from pathlib import Path

from fastapi import FastAPI, Query, Request, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.config import get_settings
from app.zoho_client import zoho_client

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
    """Polling endpoint to check if score is available."""
    settings = get_settings()
    thank_you_url = settings.thank_you_page_url or "/thank-you"

    try:
        score = await zoho_client.get_score_for_key(key)
        logger.info(f"Check score for {key}: {score}")

        if score is not None:
            # Score found - determine redirect
            if score >= settings.score_threshold:
                logger.info(f"Score {score} >= {settings.score_threshold}, ready for success redirect")
                return {"status": "ready", "redirect_url": settings.success_redirect_url}
            else:
                logger.info(f"Score {score} < {settings.score_threshold}, ready for thank you redirect")
                return {"status": "ready", "redirect_url": thank_you_url}

        # Score not found yet - keep polling
        logger.info(f"Score not found for {key}, client should keep polling")
        return {"status": "not_found", "redirect_url": thank_you_url}

    except Exception as e:
        logger.error(f"Error checking score for {key}: {e}")
        return {"status": "error", "redirect_url": thank_you_url}


@app.get("/thank-you", response_class=HTMLResponse)
async def thank_you(request: Request):
    """Display the thank you page."""
    return templates.TemplateResponse("thank_you.html", {"request": request})


@app.get("/health")
async def health_check():
    """Health check endpoint for Railway and load balancers."""
    return {"status": "healthy"}
