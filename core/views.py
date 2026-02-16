from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Project, Vendor, MasterCategory

@login_required
def owner_dashboard(request):
    return render(request, 'dashboard/owner_dashboard.html')

@login_required
def main_dashboard(request):
    # Fallback or alias for unified dashboard
    return render(request, 'dashboard/owner_dashboard.html')

@login_required
def daily_cash(request):
    return render(request, 'dashboard/daily_cash.html')

@login_required
def vendor_analytics(request):
    return render(request, 'dashboard/vendor_analytics.html')

@login_required
def master_categories(request):
    return render(request, 'master_categories.html')

@login_required
def projects(request):
    return render(request, 'projects.html')

@login_required
def vendors(request):
    return render(request, 'vendors.html')
