from django.contrib import admin

from .models import Customer,PaymentAttempt, RecoveryAction

# Register your models here.
admin.site.register(Customer)
admin.site.register(PaymentAttempt)
admin.site.register(RecoveryAction)
