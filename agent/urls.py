from django.urls import path,include
from . import views 
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('audit-trail/<int:payment_id>/', views.audit_trail, name='audit-trail'),
    path('payment-list/', views.payment_list, name='payment-list')
]