import logging
from pathlib import Path

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
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

# CORS middleware to allow form submissions from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class FormSubmission(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    work_situation: Optional[str] = None
    goal: Optional[str] = None
    driving: Optional[str] = None
    timing: Optional[str] = None
    investment: Optional[str] = None
    blocker: Optional[str] = None
    lead_score: Optional[int] = None
    time_on_page: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    ip_country: Optional[str] = None
    user_agent: Optional[str] = None
    screen_res: Optional[str] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    utm_term: Optional[str] = None
    utm_content: Optional[str] = None
    vsl_source: Optional[str] = None

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


@app.post("/backup-submission")
async def backup_submission(submission: FormSubmission):
    """Backup endpoint to log form submissions in case Zoho fails."""
    logger.info("=== BACKUP FORM SUBMISSION ===")
    logger.info(f"Name: {submission.first_name} {submission.last_name}")
    logger.info(f"Email: {submission.email}")
    logger.info(f"Phone: {submission.phone}")
    logger.info(f"Work Situation: {submission.work_situation}")
    logger.info(f"Goal: {submission.goal}")
    logger.info(f"Driving: {submission.driving}")
    logger.info(f"Timing: {submission.timing}")
    logger.info(f"Investment: {submission.investment}")
    logger.info(f"Blocker: {submission.blocker}")
    logger.info(f"Lead Score: {submission.lead_score}")
    logger.info(f"Time on Page: {submission.time_on_page}s")
    logger.info(f"Location: {submission.latitude}, {submission.longitude} ({submission.ip_country})")
    logger.info(f"User Agent: {submission.user_agent}")
    logger.info(f"Screen: {submission.screen_res}")
    logger.info(f"UTM: source={submission.utm_source}, medium={submission.utm_medium}, campaign={submission.utm_campaign}")
    logger.info(f"VSL Source: {submission.vsl_source}")
    logger.info("=== END BACKUP ===")

    return {"status": "ok", "message": "Backup received"}
