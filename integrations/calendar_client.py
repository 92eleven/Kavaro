from datetime import datetime, timedelta
from typing import Optional
from core.models import Lead, Appointment
from config import settings

class CalendarClient:
    """
    Adapter for Google Calendar booking.
    """
    def __init__(self):
        self.calendar_id = settings.GOOGLE_CALENDAR_ID

    def book_appointment(self, lead: Lead, start_time: datetime) -> Optional[Appointment]:
        """
        Books a discovery call slot for a qualified lead.
        """
        if not start_time:
            # Fallback: Tomorrow at 9 AM
            start_time = (datetime.now() + timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)

        print(f"Booking appointment for {lead.name} at {start_time}")
        
        appointment = Appointment(
            lead_id=lead.id,
            start_time=start_time,
            end_time=start_time + timedelta(minutes=30),
            summary=f"QualifAI Discovery Call: {lead.name}"
        )
        # In a real app, this would call the Google Calendar API here
        return appointment

    def is_slot_available(self, start_time: datetime) -> bool:
        """
        Checks if a given time slot is free on the calendar.
        MOCKED: Always returns True.
        """
        return True
