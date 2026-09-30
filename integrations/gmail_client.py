import smtplib
import imaplib
import email
import os
import httpx
import traceback
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
            status, messages = mail.search(None, 'UNSEEN')
            for num in messages[0].split():
                status, data = mail.fetch(num, '(RFC822)')
                for response_part in data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject = msg["subject"]
                        sender = msg["from"]
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
        Sends an email response to the lead via SendGrid.
        """
        api_key = os.environ.get("SENDGRID_API_KEY")
        print(f"SendGrid API key present: {bool(api_key)}")
        print(f"Lead email: {lead.email}")
        
        if not api_key or not lead.email:
            print("Missing API key or email — aborting send")
            return
            
        try:
            print(f"Attempting SendGrid send to {lead.email}")
            response = httpx.post(
                "https://api.sendgrid.com/v3/mail/send",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "personalizations": [{"to": [{"email": lead.email}]}],
                    "from": {"email": "kavaroai.agent@gmail.com"},
                    "subject": f"Re: {lead.metadata.get('subject', 'Your Inquiry')}",
                    "content": [{"type": "text/plain", "value": text}]
                }
            )
            print(f"SendGrid response: {response.status_code}")
            print(f"SendGrid response body: {response.text}")
        except Exception as e:
            print(f"SendGrid send error: {e}")
            traceback.print_exc()