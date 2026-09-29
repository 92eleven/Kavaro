from typing import List, Dict, Optional
from .brain import Brain
from .models import Lead, LeadStatus, LogEntry, QualificationResult, Appointment
from integrations.gmail_client import GmailClient
from integrations.twilio_client import TwilioClient
from integrations.calendar_client import CalendarClient
from feedback.logger import QualifAILogger
import datetime

class QualifAIAgent:
    """
    Main orchestrator that ties the brain and integrations together.
    """
    def __init__(self):
        self.brain = Brain()
        self.gmail = GmailClient()
        self.twilio = TwilioClient()
        self.calendar = CalendarClient()
        self.logger = QualifAILogger()
        self.integrations = {
            "gmail": self.gmail,
            "twilio": self.twilio
        }

    def process_new_leads(self):
        """
        Main loop to fetch and process leads from all configured sources.
        """
        for source_name, integration in self.integrations.items():
            new_leads = integration.fetch_new_leads()
            for lead in new_leads:
                self.handle_lead(lead)

    def handle_lead(self, lead: Lead, message_text: str = None):
        """
        Single lead interaction handler.
        """
        print(f"Handling lead: {lead.id} from {lead.source}")
        
        # 1. Get response from Brain
        history = lead.metadata.get("history", [])
        
        qualification_result = self.brain.qualify_text(
            lead=lead, 
            text=message_text or "Initial Contact", 
            history=history
        )
        
        # 2. Handle qualification and immediate booking
        appointment = None
        if qualification_result.is_qualified:
            appointment = self.qualify_and_book(lead, qualification_result)
            if appointment:
                booking_note = f"\n\nI've gone ahead and booked a 30-minute discovery call for us on {appointment.start_time.strftime('%A, %b %d at %I:%M %p')}. Looking forward to it!"
                qualification_result.response_text += booking_note

        # Update history in metadata
        history.append({"role": "user", "content": message_text or "Initial Contact"})
        history.append({"role": "assistant", "content": qualification_result.response_text})
        lead.metadata["history"] = history
        
        # 3. Log the interaction
        log_entry = LogEntry(
            lead_id=lead.id,
            action="respond",
            input_text=message_text or "Initial Contact",
            output_text=qualification_result.response_text,
            outcome="Booked" if appointment else ("Qualified" if qualification_result.is_qualified else "Qualifying")
        )
        self.logger.log(log_entry)
        
        # 4. Send response back (including booking info if qualified)
        if lead.source in self.integrations:
            self.integrations[lead.source].send_message(lead, qualification_result.response_text)

    def qualify_and_book(self, lead: Lead, qualification_result: QualificationResult) -> Optional[Appointment]:
        """
        Finalizes the qualification and triggers the booking process.
        """
        print(f"Qualifying and booking lead: {lead.id}")
        lead.status = LeadStatus.QUALIFIED
        
        # Generate 3 potential slots starting tomorrow at 9am, 10am, 11am
        from datetime import datetime, time, timedelta
        tomorrow = datetime.now().date() + timedelta(days=1)
        potential_slots = [
            datetime.combine(tomorrow, time(9, 0)),
            datetime.combine(tomorrow, time(10, 0)),
            datetime.combine(tomorrow, time(11, 0))
        ]
        
        selected_slot = None
        for slot in potential_slots:
            if self.calendar.is_slot_available(slot):
                selected_slot = slot
                break
        
        if selected_slot:
            appointment = self.calendar.book_appointment(lead, selected_slot)
            lead.status = LeadStatus.BOOKED
            print(f"Lead {lead.id} successfully booked for {selected_slot}")
            return appointment
        else:
            print(f"No slots available for lead {lead.id}")
            return None
