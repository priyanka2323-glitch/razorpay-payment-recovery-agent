from .models import RecoveryAction
from .decision import decide_action
from .guardrails import apply_guardrails
from .executor import execute_action

STOPPING_OUTCOMES = ["success", "escalated", "stopped"]

def run_recovery(payment, max_loops=5):
    """Runs the act-observe-decide loop for a single payment until it stops."""
    customer = payment.customer
    log = []

    for _ in range(max_loops):
        if payment.status == "success":
            break

        attempt_history = list(
            RecoveryAction.objects.filter(payment=payment).values(
                "action_taken", "outcome"
            )
        )

        decision = decide_action(payment, customer, attempt_history)
        final_action, reasoning = apply_guardrails(decision, payment, customer)
        outcome = execute_action(payment, final_action, reasoning)

        log.append({"action": final_action, "reasoning": reasoning, "outcome": outcome})

        if outcome in STOPPING_OUTCOMES:
            break

    return log