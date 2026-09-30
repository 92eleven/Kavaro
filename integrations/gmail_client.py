import smtplib
import imaplib
import email
import os
import httpx
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

    def send_sendgrid(self, to_email: str, subject: str, body: str):
        """
        Reusable SendGrid email sender.
        """
        api_key = os.environ.get("SENDGRID_API_KEY")
        if not api_key:
            print("Missing SendGrid API key")
            return
        try:
            response = httpx.post(
                "https://api.sendgrid.com/v3/mail/send",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "personalizations": [{"to": [{"email": to_email}]}],
                    "from": {"email": "kavaroai.agent@gmail.com"},
                    "subject": subject,
                    "content": [{"type": "text/plain", "value": body}]
                }
            )
            print(f"SendGrid response to {to_email}: {response.status_code}")
        except Exception as e:
            print(f"SendGrid send error: {e}")

    def send_message(self, lead: Lead, text: str):
        """
        Sends qualification response to lead and notifies owner.
        """
        # Send response to lead
        self.send_sendgrid(
            to_email=lead.email,
            subject=f"Re: {lead.metadata.get('subject', 'Your Inquiry')}",
            body=text
        )

        # Notify owner
        owner_email = "kavaroai.agent@gmail.com"
        owner_body = (
            f"New lead received!\n\n"
            f"Name: {lead.name}\n"
            f"Email: {lead.email}\n"
            f"Source: {lead.source}\n\n"
            f"AI Response Sent:\n{text}"
        )
        self.send_sendgrid(
            to_email=owner_email,
            subject=f"New Lead: {lead.name} ({lead.email})",
            body=owner_body
        )