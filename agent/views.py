from django.shortcuts import render

# Create your views here.

from django.db.models import Sum, Count,Q
from .models import PaymentAttempt, RecoveryAction

def dashboard(request):
    all_payments = PaymentAttempt.objects.all()
    total_at_risk = all_payments.aggregate(total=Sum("amount"))["total"] or 0

    recovered_payments = all_payments.filter(status="success")
    total_recovered = recovered_payments.aggregate(total=Sum("amount"))["total"] or 0

    total_count = all_payments.count()
    recovered_count = recovered_payments.count()
    recovery_rate = round((recovered_count / total_count) * 100, 1) if total_count else 0

    # Breakdown by failure code
    breakdown = (
        all_payments.values("failure_code")
        .annotate(total=Count("id"), recovered=Count("id", filter=__import__("django.db.models").db.models.Q(status="success")))
    )

    # Action distribution (for a pie/bar chart)
    action_counts = (
        RecoveryAction.objects.values("action_taken")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    context = {
        "total_at_risk": total_at_risk,
        "total_recovered": total_recovered,
        "recovery_rate": recovery_rate,
        "total_count": total_count,
        "recovered_count": recovered_count,
        "breakdown": breakdown,
        "action_labels": [a["action_taken"] for a in action_counts],
        "action_data": [a["count"] for a in action_counts],
    }
    return render(request, "agent/dashboard.html", context)


def audit_trail(request, payment_id):
    payment = PaymentAttempt.objects.get(id=payment_id)
    actions = RecoveryAction.objects.filter(payment=payment).order_by("timestamp")
    return render(request, "agent/audit_trail.html", {"payment": payment, "actions": actions})


def payment_list(request):
    payments = PaymentAttempt.objects.select_related("customer").all()[:100]
    return render(request, "agent/payment_test.html", {"payments": payments})