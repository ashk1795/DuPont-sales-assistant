import openai
from config import OPENAI_KEY
from typing import Dict, List, Union

openai.api_key = OPENAI_KEY

def _build_prompt(lead: Dict) -> str:
    return (
        f"""
Write a concise, friendly professional outreach email introducing DuPont Tedlar to {lead.get('contact_name', 'the contact')} (title: {lead.get('title', '')}) at {lead.get('company', '')}.
Reference the event: {lead.get('event', '')}.
Explain why this company/contact is relevant: {lead.get('rationale', '')}.
The product is Tedlar (durable films for signage and graphics).
Format as a plain text email with subject and signature.
"""
    )

def generate_outreach_note(lead_or_leads: Union[Dict, List[Dict]]) -> Union[str, List[str]]:
    """
    Generate personalized outreach email(s) for one or more leads.
    Each lead dict should have: company, contact_name, title, event, rationale.
    Returns a string (single) or list of strings (batch).
    """
    def generate_single(lead: Dict) -> str:
        prompt = _build_prompt(lead)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.7,
            )
            return response.choices[0].message['content'].strip()
        except Exception as e:
            return f"[Error generating outreach: {e}]"

    if isinstance(lead_or_leads, dict):
        return generate_single(lead_or_leads)
    elif isinstance(lead_or_leads, list):
        return [generate_single(lead) for lead in lead_or_leads]
    else:
        raise ValueError("Input must be a dict or list of dicts.")