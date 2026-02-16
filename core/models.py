from django.db import models
from django.utils import timezone

class MasterCategory(models.Model):
    """Master Category for grouped expenses/materials"""
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    TYPE_CHOICES = [
        ('MATERIAL', 'Material'),
        ('EXPENSE', 'Expense'),
    ]
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'master_category'
        verbose_name_plural = 'Master Categories'

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    """Subcategories for MasterCategory"""
    subcategory_id = models.AutoField(primary_key=True)
    parent_category = models.ForeignKey(MasterCategory, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    default_unit = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'sub_category'
        verbose_name_plural = 'Sub Categories'

    def __str__(self):
        return self.name

class Project(models.Model):
    """Project model with status tracking"""
    project_id = models.AutoField(primary_key=True)
    company = models.ForeignKey('users.Company', on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    budget = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    STATUS_CHOICES = [
        ('PLANNING', 'Planning'),
        ('ACTIVE', 'Active'),
        ('ON_HOLD', 'On Hold'),
        ('COMPLETED', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANNING')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'project'

    def __str__(self):
        return self.name

class Vendor(models.Model):
    """Vendor model for company-specific vendors"""
    vendor_id = models.AutoField(primary_key=True)
    company = models.ForeignKey('users.Company', on_delete=models.CASCADE, related_name='vendors')
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=120, blank=True, null=True)
    gst_number = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vendor'

    def __str__(self):
        return self.name
