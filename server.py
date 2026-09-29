import uvicorn
from fastapi import FastAPI, Request, BackgroundTasks, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
from typing import Optional
from core.agent import QualifAIAgent
from core.models import Lead, LeadStatus
from config import settings
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("QualifAI-Webhook")

app = FastAPI(title="QualifAI Webhook Server")
_agent = None

def get_agent():
    global _agent
    if _agent is None:
        _agent = QualifAIAgent()
    return _agent

# Pydantic models for validation
class GmailWebhook(BaseModel):
    email: EmailStr
    name: Optional[str] = "Prospect"
    message: str

class TwilioWebhook(BaseModel):
    # Twilio sends form data, but we can use this for internal processing
    # if we ever switch to JSON or just for documentation.
    From: str
    Body: str

async def verify_secret(
    x_qualifai_secret: Optional[str] = Header(None),
    secret: Optional[str] = None
):
    """
    Optional security check if WEBHOOK_SECRET is configured.
    Checks both X-QualifAI-Secret header and 'secret' query parameter.
    """
    provided_secret = x_qualifai_secret or secret
    if settings.WEBHOOK_SECRET and provided_secret != settings.WEBHOOK_SECRET:
        logger.warning(f"Unauthorized access attempt with secret: {provided_secret}")
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/health")
def health_check():
    return {"status": "ok", "app": "QualifAI"}

@app.post("/webhook/gmail", dependencies=[Depends(verify_secret)])
async def webhook_gmail(data: GmailWebhook, background_tasks: BackgroundTasks):
    """
    Inbound Gmail webhook handler.
    Expected JSON payload: { "email": "...", "name": "...", "message": "..." }
    """
    logger.info(f"Received Gmail webhook for: {data.email}")
    
    lead = Lead(
        id=f"gmail-{data.email}",
        email=data.email,
        name=data.name or "Prospect",
        source="gmail"
    )
    
    background_tasks.add_task(safe_handle_lead, lead, data.message)
    return {"status": "accepted"}

@app.post("/webhook/twilio", dependencies=[Depends(verify_secret)])
async def webhook_twilio(request: Request, background_tasks: BackgroundTasks):
    """
    Inbound Twilio SMS webhook handler.
    Twilio sends application/x-www-form-urlencoded data.
    """
    try:
        form_data = await request.form()
        from_number = form_data.get("From")
        body = form_data.get("Body", "")
        
        if not from_number:
            raise HTTPException(status_code=400, detail="Missing 'From' field")

        logger.info(f"Received Twilio webhook from: {from_number}")
        
        lead = Lead(
            id=f"twilio-{from_number}",
            phone=from_number,
            name="SMS Prospect",
            source="twilio"
        )
        
        background_tasks.add_task(safe_handle_lead, lead, body)
        return {"status": "accepted"}
    except Exception as e:
        logger.error(f"Error processing Twilio webhook: {e}")
        raise HTTPException(status_code=400, detail="Invalid form data")

async def safe_handle_lead(lead: Lead, message: str):
    """
    Wrapper for agent.handle_lead to ensure background errors are logged.
    """
    try:
        get_agent().handle_lead(lead, message)
    except Exception as e:
        logger.error(f"Error in background task for lead {lead.id}: {e}", exc_info=True)

def start_server():
    logger.info(f"Starting QualifAI Webhook Server on {settings.WEBHOOK_HOST}:{settings.WEBHOOK_PORT}")
    uvicorn.run(app, host=settings.WEBHOOK_HOST, port=settings.WEBHOOK_PORT)

if __name__ == "__main__":
    start_server()
