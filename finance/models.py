from django.db import models
from django.utils import timezone

class Expense(models.Model):
    """Unified Expense model (merging Expenses and Purchases)"""
    expense_id = models.AutoField(primary_key=True)
    company = models.ForeignKey('users.Company', on_delete=models.CASCADE, related_name='expenses')
    project = models.ForeignKey('core.Project', on_delete=models.CASCADE, related_name='expenses')
    vendor = models.ForeignKey('core.Vendor', on_delete=models.CASCADE, related_name='expenses', null=True, blank=True)
    
    expense_type = models.CharField(max_length=100) # 'Regular Expense' or 'Material Purchase'
    category = models.CharField(max_length=100, blank=True, null=True) # Main category from MasterCategory
    
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_mode = models.CharField(max_length=20) # CASH, BANK, UPI, CREDIT
    expense_date = models.DateField() # Date of expense or invoice
    
    description = models.TextField(blank=True, null=True)
    invoice_number = models.CharField(max_length=100, blank=True, null=True)
    bill_url = models.CharField(max_length=500, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'expense'

    def __str__(self):
        return f'{self.expense_type} - {self.amount}'

class ExpenseItem(models.Model):
    """Expense item model for line items"""
    expense_item_id = models.AutoField(primary_key=True)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    measuring_unit = models.CharField(max_length=20, default='Unit')
    unit_price = models.DecimalField(max_digits=15, decimal_places=2)
    total_price = models.DecimalField(max_digits=15, decimal_places=2)
    brand = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'expense_item'

    def __str__(self):
        return self.item_name

class Payment(models.Model):
    """Payment model for vendor payments"""
    payment_id = models.AutoField(primary_key=True)
    company = models.ForeignKey('users.Company', on_delete=models.CASCADE, related_name='payments')
    vendor = models.ForeignKey('core.Vendor', on_delete=models.CASCADE, related_name='payments')
    project = models.ForeignKey('core.Project', on_delete=models.CASCADE, related_name='payments')
    expense = models.ForeignKey(Expense, on_delete=models.SET_NULL, related_name='payments', null=True, blank=True)
    
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_date = models.DateField()
    payment_mode = models.CharField(max_length=20)  # CASH, BANK, UPI
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payment'

    def __str__(self):
        return f'Payment {self.amount}'

class ClientPayment(models.Model):
    """Client payment model for incoming payments"""
    client_payment_id = models.AutoField(primary_key=True)
    company = models.ForeignKey('users.Company', on_delete=models.CASCADE, related_name='client_payments')
    project = models.ForeignKey('core.Project', on_delete=models.CASCADE, related_name='client_payments')
    
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_date = models.DateField()
    payment_mode = models.CharField(max_length=20)  # CASH, BANK, UPI
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'client_payment'

    def __str__(self):
        return f'ClientPayment {self.amount}'
