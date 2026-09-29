import json
from typing import List, Optional, Dict
from .models import QualificationResult, Lead
from config import settings

class Brain:
    """
    The reasoning engine for lead qualification.
    """
    def __init__(self, knowledge_base_path: str = "knowledge_base.json"):
        try:
            with open(knowledge_base_path, 'r') as f:
                self.kb = json.load(f)
        except FileNotFoundError:
            self.kb = {}
            
    def get_system_prompt(self) -> str:
        """
        Generates the system prompt based on knowledge base and company settings.
        """
        criteria = "\n".join([f"- {c}" for c in self.kb.get("qualification_criteria", [])])
        return f"""
You are an expert Lead Qualification Agent for {settings.COMPANY_NAME}.
Your goal is to qualify inbound leads based on specific criteria and book appointments for qualified leads.

COMPANY INFO:
{settings.COMPANY_DESCRIPTION}

QUALIFICATION CRITERIA:
{criteria}

INSTRUCTIONS:
1. Be professional, helpful, and concise.
2. Answer questions using the FAQ provided below.
3. If a lead meets ALL criteria, suggest booking a call using this link: {settings.BOOKING_LINK}
4. If they don't meet criteria, politely decline or offer a resource.
5. If you need more information to qualify them, ask follow-up questions one at a time.
6. IF lead budget is unknown after 2 messages, ASK: 'What is your monthly budget for consulting services?'

FAQ:
{json.dumps(self.kb.get("faqs", []), indent=2)}
"""

    def qualify_text(self, lead: Lead, text: str, history: List[Dict[str, str]] = []) -> QualificationResult:
        """
        Qualifies a lead based on input text and interaction history using OpenAI.
        """
        try:
            from openai import OpenAI
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            
            system_prompt = self.get_system_prompt()
            system_prompt += "\n\nYou must respond in valid JSON format. Response should strictly match this structure: {\"is_qualified\": bool, \"reasoning\": \"string\", \"response_text\": \"string\", \"suggested_next_action\": \"string\", \"objections_handled\": [\"string\"]}"

            messages = [{"role": "system", "content": system_prompt}]
            
            # Add conversation history
            for entry in history:
                messages.append(entry)
            
            # Add current message
            messages.append({"role": "user", "content": f"Lead Info: {lead.name} ({lead.email or lead.phone})\nLatest Message: {text}"})

            response = client.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=messages,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            result_data = json.loads(content)
            
            return QualificationResult(**result_data)

        except Exception as e:
            print(f"Brain: Error during qualification: {e}")
            return QualificationResult(
                is_qualified=False,
                reasoning=f"Technical error: {str(e)}",
                response_text="I'm having a bit of technical trouble at the moment, but I'll get back to you as soon as possible.",
                suggested_next_action="Continue qualifying manually or ask follow-up questions."
            )

    def get_faq_answer(self, question: str) -> Optional[str]:
        """
        Retrieves an answer from the FAQ based on keyword matching.
        """
        for faq in self.kb.get("faqs", []):
            if faq["question"].lower() in question.lower():
                return faq["answer"]
        return None
