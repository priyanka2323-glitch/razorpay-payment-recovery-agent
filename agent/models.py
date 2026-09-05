

from django.db import models

# Create your models here.
class Customer(models.Model):
    name=models.CharField(max_length=50)
    phone=models.CharField(max_length=15)
    email=models.EmailField()
    preferred_channel=models.CharField(max_length=20,default='email')
    dnd=models.BooleanField(default=False)
class PaymentAttempt(models.Model):
    FAILURE_CODES = [
        ("insufficient_funds", "Insufficient Funds"),
        ("expired_card", "Expired Card"),
        ("bank_timeout", "Bank Timeout"),
        ("do_not_honor", "Do Not Honor"),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="failed")  # failed/success
    failure_code = models.CharField(max_length=30, choices=FAILURE_CODES, blank=True)
    attempt_number = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
class RecoveryAction(models.Model):
    payment=models.ForeignKey(PaymentAttempt,on_delete=models.CASCADE)
    action_taken=models.CharField(max_length=100)
    reasoning=models.TextField(max_length=50)
    outcome=models.CharField(max_length=50,blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)