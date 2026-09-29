import sys
import os
from datetime import datetime

# Add the project root to sys.path
sys.path.append(os.getcwd())

from core.agent import QualifAIAgent
from core.models import Lead, QualificationResult, LeadStatus
from unittest.mock import MagicMock

def test_booking_flow():
    print("Starting booking flow test...")
    
    agent = QualifAIAgent()
    
    # Mock the brain's qualify_text method to return a qualified result
    agent.brain.qualify_text = MagicMock(return_value=QualificationResult(
        is_qualified=True,
        reasoning="Lead meets all criteria.",
        response_text="You look like a great fit! I'd love to chat.",
        suggested_next_action="Book a call",
        objections_handled=[]
    ))
    
    # Mock integration to avoid actual network calls
    mock_integration = MagicMock()
    agent.integrations["test_source"] = mock_integration
    
    # Create a test lead
    lead = Lead(
        id="test_lead_123",
        name="Test User",
        email="test@example.com",
        source="test_source",
        status=LeadStatus.NEW
    )
    
    # Handle the lead
    agent.handle_lead(lead, message_text="I have 50 leads per month and a $10k budget.")
    
    # Assertions
    print(f"Lead status: {lead.status}")
    assert lead.status == LeadStatus.BOOKED
    
    # Check if messages were "sent"
    assert mock_integration.send_message.call_count == 2
    
    # Check logs
    logs = agent.logger.get_logs()
    booked_log = next((log for log in logs if log.get("outcome") == "Booked"), None)
    assert booked_log is not None
    assert booked_log["lead_id"] == "test_lead_123"
    
    print("Test passed! Booking flow is working as expected.")

if __name__ == "__main__":
    test_booking_flow()
