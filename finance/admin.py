from django.contrib import admin
from .models import Expense, ExpenseItem, Payment, ClientPayment

class ExpenseItemInline(admin.TabularInline):
    model = ExpenseItem
    extra = 1

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('expense_id', 'project', 'vendor', 'expense_type', 'amount', 'payment_mode', 'expense_date')
    list_filter = ('company', 'project', 'vendor', 'expense_type', 'payment_mode')
    search_fields = ('description', 'invoice_number')
    inlines = [ExpenseItemInline]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'project', 'vendor', 'amount', 'payment_mode', 'payment_date')
    list_filter = ('company', 'project', 'vendor', 'payment_mode')

@admin.register(ClientPayment)
class ClientPaymentAdmin(admin.ModelAdmin):
    list_display = ('client_payment_id', 'project', 'amount', 'payment_mode', 'payment_date')
    list_filter = ('company', 'project', 'payment_mode')
