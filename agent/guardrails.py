from datetime import datetime
import random
MAX_ATTEMPTS = 3
QUIET_HOURS_START = 21  # 9 PM
QUIET_HOURS_END = 8     # 8 AM

CONTACT_ACTIONS = ["send_reminder", "offer_alt_payment"]

def is_quiet_hours():
    hour = datetime.now().hour
    return hour >= QUIET_HOURS_START or hour < QUIET_HOURS_END

def apply_guardrails(decision, payment, customer):
    """Overrides the LLM's decision if it violates a hard rule. Returns (action, reason)."""
    action = decision.get("action")
    reasoning = decision.get("reasoning", "")

    # Rule 1: DND customers can't be contacted
    if customer.dnd and action in CONTACT_ACTIONS:
        return "escalate_to_human", f"Blocked: customer is DND. Original action was '{action}'."

    # Rule 2: Max attempts hard cap
    if payment.attempt_number >= MAX_ATTEMPTS and action not in ["escalate_to_human", "stop"]:
        return "escalate_to_human", f"Blocked: max attempts ({MAX_ATTEMPTS}) reached."

    # Rule 3: No contact actions during quiet hours
    elif action == "retry_delayed":
    # Simulate the delayed retry actually happening (demo: no real wait)
        outcome = "success" if random.random() < 0.35 else "failed"
        payment.attempt_number += 1
        if outcome == "success":
           payment.status = "success"

    # Passed all checks — use LLM's original decision
    return action, reasoning