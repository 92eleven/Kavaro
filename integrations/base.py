from abc import ABC, abstractmethod
from typing import List
from core.models import Lead

class BaseIntegration(ABC):
    """
    Abstract base class for all external service integrations.
    """
    @abstractmethod
    def fetch_new_leads(self) -> List[Lead]:
        """Fetch new inbound leads from the source."""
        pass

    @abstractmethod
    def send_message(self, lead: Lead, text: str):
        """Send a message back to the lead."""
        pass
