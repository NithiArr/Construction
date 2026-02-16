from django.urls import path
from . import views
from . import api
from core import export_utils

urlpatterns = [
    # Pages
    path('expenses', views.expenses, name='expenses'),
    path('purchases', views.purchases, name='purchases'),
    path('payments', views.payments, name='payments'),
    path('client-payments', views.client_payments, name='client_payments'),
    
    # APIs
    
    # Export endpoints (Must come before generic ID patterns)
    path('api/expenses/export', export_utils.export_expenses_to_excel, name='export_expenses'),
    path('api/purchases/export', export_utils.export_purchases_to_excel, name='export_purchases'),
    path('api/payments/export', export_utils.export_vendor_payments_to_excel, name='export_vendor_payments'),
    path('api/client-payments/export', export_utils.export_client_payments_to_excel, name='export_client_payments'),
    path('api/expenses', api.expenses_list, name='api_expenses_list'),
    path('api/expenses/<str:expense_id>', api.expense_detail, name='api_expense_detail'),
    
    path('api/purchases', api.purchases_list, name='api_purchases_list'),
    path('api/purchases/<str:purchase_id>', api.purchase_detail, name='api_purchase_detail'),
    
    path('api/payments', api.payments_list, name='api_payments_list'),
    path('api/payments/<str:payment_id>', api.payment_detail, name='api_payment_detail'),
    
    path('api/client-payments', api.client_payments_list, name='api_client_payments_list'),
    path('api/client-payments/<str:client_payment_id>', api.client_payment_detail, name='api_client_payment_detail'),
    
    
]
