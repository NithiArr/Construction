from django.contrib import admin
from .models import Project, Vendor, MasterCategory, SubCategory

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'status', 'budget', 'start_date', 'end_date')
    list_filter = ('company', 'status')
    search_fields = ('name', 'location')

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'phone', 'email', 'gst_number')
    list_filter = ('company',)
    search_fields = ('name', 'email', 'phone')

class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1

@admin.register(MasterCategory)
class MasterCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'is_active')
    list_filter = ('type', 'is_active')
    search_fields = ('name',)
    inlines = [SubCategoryInline]
