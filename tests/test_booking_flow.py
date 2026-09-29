import sys
import os
from datetime import datetime, timedelta
from unittest.mock import MagicMock

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.agent import QualifAIAgent
from core.models import Lead, LeadStatus, QualificationResult
from core.brain import Brain

def test_booking_flow():
    print("Testing end-to-end booking flow...")
    agent = QualifAIAgent()
    
    # Mock brain to always qualify the lead
    agent.brain.qualify_text = MagicMock(return_value=QualificationResult(
        is_qualified=True,
        reasoning="Lead meets all criteria.",
        response_text="You sound like a great fit! I'd love to schedule a call.",
        suggested_next_action="Book a call",
        objections_handled=[]
    ))
    
    # Mock integration to avoid actual sending
    mock_integration = MagicMock()
    agent.integrations["gmail"] = mock_integration
    
    # Create a test lead
    lead = Lead(
        id="test-booking-123",
        name="Alice Smith",
        email="alice@example.com",
        source="gmail",
        status=LeadStatus.NEW
    )
    
    # Process the lead
    agent.handle_lead(lead, "I am interested in your services and have a budget of $10k.")
    
    # Assertions
    print(f"Lead status: {lead.status}")
    assert lead.status == LeadStatus.BOOKED
    
    # Check if message was "sent" (mocked)
    assert mock_integration.send_message.called
    sent_msg = mock_integration.send_message.call_args[0][1]
    print(f"Sent message: {sent_msg}")
    assert "booked a 30-minute discovery call" in sent_msg
    
    # Check logs
    import json
    log_file = f"logs/logs_{datetime.utcnow().strftime('%Y-%m-%d')}.jsonl"
    with open(log_file, "r") as f:
        logs = [json.loads(line) for line in f]
    
    booking_log = next((l for l in logs if l["lead_id"] == "test-booking-123" and l["outcome"] == "Booked"), None)
    assert booking_log is not None
    print(f"Found booking log: {booking_log}")
    
    print("Test passed!")

if __name__ == "__main__":
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)
    test_booking_flow()
