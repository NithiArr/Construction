from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Company, User


def home(request):
    if request.user.is_authenticated:
        # Route by role to prevent unauthorized redirect bounces
        if request.user.role == 'EMPLOYEE':
            return redirect('purchases')
        elif request.user.role == 'MANAGER':
            return redirect('daily_cash')
        else: # ADMIN
            return redirect('owner_dashboard')
    return redirect('login')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f"Attempting login for: {email}")
        user = authenticate(request, username=email, password=password)
        print(f"Authenticate result: {user}")

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.name}!")
            return redirect('home')
        else:
            print("Authentication failed.")
            messages.error(request, "Invalid email or password.")

    companies = Company.objects.all()
    return render(request, 'login.html', {'companies': companies})


def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')


@login_required
def register_view(request):
    """ADMIN-only: Create a new user (ADMIN, MANAGER, or EMPLOYEE).
    - Can only be accessed by existing ADMINs
    - Automatically assigns user to the current Admin's company
    """
    if request.user.role != 'ADMIN':
        messages.error(request, "You don't have permission to register new users.")
        return redirect('home')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        role = request.POST.get('role', '')

        form_data = {'name': name, 'email': email, 'role': role}

        # Validation
        if not all([name, email, password, role]):
            messages.error(request, "All fields are required.")
            return render(request, 'register.html', {'form_data': form_data})

        if role not in ('ADMIN', 'MANAGER', 'EMPLOYEE'):
            messages.error(request, "Invalid role selected.")
            return render(request, 'register.html', {'form_data': form_data})

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html', {'form_data': form_data})

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return render(request, 'register.html', {'form_data': form_data})

        if User.objects.filter(email=email).exists():
            messages.error(request, f"A user with email '{email}' already exists.")
            return render(request, 'register.html', {'form_data': form_data})

        # All users get assigned to the Admin's company automatically
        company = request.user.company

        # Create user
        user = User.objects.create_user(
            email=email,
            password=password,
            name=name,
            role=role,
            company=company,
        )

        messages.success(request, f"User '{user.name}' ({user.get_role_display()}) created successfully!")
        return redirect('manage_users')

    return render(request, 'register.html', {'form_data': {}})


@login_required
def manage_users_view(request):
    """ADMIN-only: view all users in the same company."""
    if request.user.role != 'ADMIN':
        messages.error(request, "Only admins can manage users.")
        return redirect('purchases')

    users = User.objects.filter(company=request.user.company).order_by('role', 'name')
    return render(request, 'manage_users.html', {'users': users})


@login_required
def delete_user_view(request, user_id):
    """ADMIN-only: delete a user (cannot delete yourself)."""
    if request.user.role != 'ADMIN':
        messages.error(request, "Only admins can delete users.")
        return redirect('purchases')

    if request.method == 'POST':
        user = get_object_or_404(User, user_id=user_id, company=request.user.company)
        if user.pk == request.user.pk:
            messages.error(request, "You cannot delete your own account.")
        else:
            name = user.name
            user.delete()
            messages.success(request, f"User '{name}' has been deleted.")

    return redirect('manage_users')
