import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from typing import List
from .base import BaseIntegration
from core.models import Lead
from config import settings

class GmailClient(BaseIntegration):
    """
    Adapter for Gmail using IMAP and SMTP.
    """
    def __init__(self):
        self.user = settings.GMAIL_USER
        self.password = settings.GMAIL_PASSWORD

    def fetch_new_leads(self) -> List[Lead]:
        """
        Fetches unread emails and converts them to Lead objects.
        """
        if not self.user or not self.password:
            return []
            
        leads = []
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(self.user, self.password)
            mail.select("inbox")
            
            # Search for unread emails
            status, messages = mail.search(None, 'UNSEEN')
            for num in messages[0].split():
                status, data = mail.fetch(num, '(RFC822)')
                for response_part in data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject = msg["subject"]
                        sender = msg["from"]
                        # Extract basic info
                        leads.append(Lead(
                            id=f"gmail_{num.decode()}",
                            email=sender,
                            name=sender.split('<')[0].strip(),
                            source="gmail",
                            metadata={"subject": subject}
                        ))
            mail.close()
            mail.logout()
        except Exception as e:
            print(f"Gmail fetch error: {e}")
            
        return leads

    def send_message(self, lead: Lead, text: str):
        """
        Sends an email response to the lead.
        """
        if not self.user or not self.password or not lead.email:
            return
            
        try:
            msg = MIMEText(text)
            msg["Subject"] = f"Re: {lead.metadata.get('subject', 'Your Inquiry')}"
            msg["From"] = self.user
            msg["To"] = lead.email
            
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.user, self.password)
                server.send_message(msg)
        except Exception as e:
            print(f"Gmail send error: {e}")
