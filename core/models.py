from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum

class LeadStatus(str, Enum):
    NEW = "new"
    QUALIFYING = "qualifying"
    QUALIFIED = "qualified"
    UNQUALIFIED = "unqualified"
    BOOKED = "booked"

class Lead(BaseModel):
    """
    Data model for a prospective lead.
    """
    id: str
    email: Optional[str] = None
    phone: Optional[str] = None
    name: Optional[str] = "Prospect"
    source: str # e.g., "gmail", "twilio"
    status: LeadStatus = LeadStatus.NEW
    metadata: Dict = {}

class QualificationResult(BaseModel):
    """
    Result of the brain's qualification process.
    """
    is_qualified: bool
    reasoning: str
    response_text: str
    suggested_next_action: str
    objections_handled: List[str] = []

class Appointment(BaseModel):
    """
    Data model for a booked appointment.
    """
    lead_id: str
    start_time: datetime
    end_time: datetime
    summary: str

class LogEntry(BaseModel):
    """
    Data model for interaction logging.
    """
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    lead_id: str
    action: str
    input_text: str
    output_text: str
    outcome: Optional[str] = None # e.g. "Qualified", "Booked"
