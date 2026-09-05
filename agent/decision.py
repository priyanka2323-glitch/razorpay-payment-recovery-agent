from curses import raw
import os
import json
from groq import Groq
from dotenv import load_dotenv
from .rag import retrieve_playbook
from .classifier import classify_failure
import re

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

ALLOWED_ACTIONS = ["retry_now", "retry_delayed", "send_reminder", "offer_alt_payment", "escalate_to_human", "stop"]

# Good free-tier Groq models: "llama-3.3-70b-versatile" or "llama-3.1-8b-instant"
MODEL_NAME = "openai/gpt-oss-120b"


def extract_json(text):
    """Extracts the first JSON object from a string, if present."""
    match = re.search(r"\{.*?\}", text, re.DOTALL)
    if match:
        return match.group(0)
    return text


def decide_action(payment, customer, attempt_history):
    playbook = retrieve_playbook(payment.failure_code)
    classification = classify_failure(payment.failure_code)

    context = f"""
Failure code: {payment.failure_code}
Classification: {classification}
Customer DND status: {customer.dnd}
Customer preferred channel: {customer.preferred_channel}
Attempt number so far: {payment.attempt_number}
Playbook guidance:
{playbook[0] if playbook else "No playbook found"}

Past attempts on this payment: {attempt_history}
"""

    prompt = f"""You are a payment recovery agent. Based on the context below, choose EXACTLY ONE action from this list:
{ALLOWED_ACTIONS}

Rules:
- If customer.dnd is True, never choose send_reminder or offer_alt_payment via contact — prefer retry_now/retry_delayed or escalate_to_human
- Never exceed 3 total attempts — if attempt_number >= 3, choose escalate_to_human or stop
- Respond ONLY in valid JSON, nothing else, no markdown fences: {{"action": "...", "reasoning": "..."}}

Context:
{context}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        max_tokens=300,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    raw = extract_json(raw)

    try:
        decision = json.loads(raw)
    except json.JSONDecodeError:
        decision = {"action": "escalate_to_human", "reasoning": f"Failed to parse LLM response: {raw[:200]}"}
        # Safety net: force a valid action even if the model hallucinates one
        if decision.get("action") not in ALLOWED_ACTIONS:
            decision = {"action": "escalate_to_human", "reasoning": f"Invalid action returned: {decision.get('action')}"}

    if decision.get("action") not in ALLOWED_ACTIONS:
        decision = {"action": "escalate_to_human", "reasoning": f"Invalid action returned: {decision.get('action')}"}

    return decision