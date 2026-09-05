from django.urls import path,include
from . import views 
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('audit-trail/<int:payment_id>/', views.audit_trail, name='audit-trail'),
    path('payment-list/', views.payment_list, name='payment-list'),
    path('api/dashboard/', views.api_dashboard, name='api_dashboard'),
    path('api/payments/', views.api_payments, name='api_payments'),
    path('api/audit/<int:payment_id>/', views.api_audit_trail, name='api_audit_trail'),
    path("seed/", views.seed_data, name="seed_data"),
    path("fixschema/", views.fix_schema, name="fix_schema"),
    ]