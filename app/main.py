import logging
from pathlib import Path

from fastapi import FastAPI, Query, Request, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
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


@app.get("/", response_class=RedirectResponse)
async def route_by_score(
    request: Request,
    key: str = Query(..., description="Key to look up in Zoho CRM"),
):
    # Log incoming request details
    logger.info("=== INCOMING REQUEST ===")
    logger.info(f"URL: {request.url}")
    logger.info(f"Method: {request.method}")
    logger.info(f"Client: {request.client}")
    logger.info(f"Headers:")
    for name, value in request.headers.items():
        logger.info(f"  {name}: {value}")

    settings = get_settings()

    try:
        score = await zoho_client.get_score_for_key(key)
        logger.info(f"Score for {key}: {score}")

        if score is not None and score >= settings.score_threshold:
            logger.info(f"Score {score} >= {settings.score_threshold}, redirecting to success URL")
            return RedirectResponse(url=settings.success_redirect_url, status_code=302)

        logger.info(f"Score {score} < {settings.score_threshold} or not found, redirecting to thank you")

        if settings.thank_you_page_url:
            return RedirectResponse(url=settings.thank_you_page_url, status_code=302)

        return RedirectResponse(url="/thank-you", status_code=302)

    except Exception as e:
        logger.error(f"Error looking up score for {email}: {e}")
        # On error, redirect to thank you page as a safe fallback
        if settings.thank_you_page_url:
            return RedirectResponse(url=settings.thank_you_page_url, status_code=302)
        return RedirectResponse(url="/thank-you", status_code=302)


@app.get("/thank-you", response_class=HTMLResponse)
async def thank_you(request: Request):
    """Display the thank you page."""
    return templates.TemplateResponse("thank_you.html", {"request": request})


@app.get("/health")
async def health_check():
    """Health check endpoint for Railway and load balancers."""
    return {"status": "healthy"}
