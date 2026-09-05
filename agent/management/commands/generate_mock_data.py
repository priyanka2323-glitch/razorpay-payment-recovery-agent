import random
from django.core.management.base import BaseCommand
from agent.models import Customer, PaymentAttempt

FIRST_NAMES = ["Aarav", "Priya", "Rohan", "Sneha", "Karan", "Divya", "Vikram", "Anjali"]
LAST_NAMES = ["Sharma", "Patel", "Reddy", "Nair", "Iyer", "Singh", "Gupta", "Menon"]
FAILURE_CODES = ["insufficient_funds", "expired_card", "bank_timeout", "do_not_honor"]
CHANNELS = ["email", "sms", "whatsapp"]

class Command(BaseCommand):
    help = "Generates mock customers and failed payment attempts"

    def add_arguments(self, parser):
        parser.add_argument("--customers", type=int, default=50)

    def handle(self, *args, **options):
        n = options["customers"]
        Customer.objects.all().delete()
        PaymentAttempt.objects.all().delete()

        for i in range(n):
            customer = Customer.objects.create(
                name=f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
                email=f"customer{i}@example.com",
                phone=f"9{random.randint(100000000,999999999)}",
                preferred_channel=random.choice(CHANNELS),
                dnd=random.random() < 0.1,  # 10% opted out
            )
            PaymentAttempt.objects.create(
                customer=customer,
                amount=round(random.uniform(199, 4999), 2),
                status="failed",
                failure_code=random.choice(FAILURE_CODES),
                attempt_number=1,
            )

        self.stdout.write(self.style.SUCCESS(f"Created {n} customers with failed payments"))