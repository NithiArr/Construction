from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Project, Vendor, MasterCategory
from functools import wraps


# ─── Role-based access decorator ──────────────────────────────────────────────

def role_required(*allowed_roles):
    """Decorator that restricts page access to users with the specified roles.
    Redirects to purchases page with an error message if unauthorized.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.role not in allowed_roles:
                messages.error(request, "You don't have permission to access that page.")
                return redirect('purchases')
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


# ─── Views ────────────────────────────────────────────────────────────────────

@login_required
@role_required('ADMIN')
def owner_dashboard(request):
    return render(request, 'dashboard/owner_dashboard.html')

@login_required
@role_required('ADMIN')
def main_dashboard(request):
    return render(request, 'dashboard/owner_dashboard.html')

@login_required
@role_required('ADMIN', 'MANAGER')
def daily_cash(request):
    return render(request, 'dashboard/daily_cash.html')

@login_required
@role_required('ADMIN', 'MANAGER')
def vendor_analytics(request):
    return render(request, 'dashboard/vendor_analytics.html')

@login_required
@role_required('ADMIN', 'MANAGER')
def master_categories(request):
    return render(request, 'master_categories.html')

@login_required
@role_required('ADMIN')
def projects(request):
    return render(request, 'projects.html')

@login_required
@role_required('ADMIN', 'MANAGER')
def vendors(request):
    return render(request, 'vendors.html')
