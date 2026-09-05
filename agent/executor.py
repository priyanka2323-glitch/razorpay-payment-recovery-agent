import random
import random
from .models import RecoveryAction

def execute_action(payment, action, reasoning):
    """Simulates performing the action and returns an outcome. In production, this would
    call real APIs (SMS gateway, payment retry API, etc.)"""

    outcome = "pending"

    if action == "retry_now":
        # Simulate ~40% success rate on retry
        outcome = "success" if random.random() < 0.4 else "failed"
        payment.attempt_number += 1
        if outcome == "success":
            payment.status = "success"

    elif action == "retry_delayed":
        outcome = "success" if random.random() < 0.35 else "failed"
        payment.attempt_number += 1
        if outcome == "success":
            payment.status = "success"

    elif action == "send_reminder":
        outcome = "sent"

    elif action == "offer_alt_payment":
        # Simulate ~55% success rate when alt method offered
        outcome = "success" if random.random() < 0.55 else "failed"
        if outcome == "success":
            payment.status = "success"

    elif action == "escalate_to_human":
        outcome = "escalated"

    elif action == "stop":
        outcome = "stopped"

    payment.save()

    # Log to audit trail
    RecoveryAction.objects.create(
        payment=payment,
        action_taken=action,
        reasoning=reasoning,
        outcome=outcome,
    )

    return outcome