from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Company

def home(request):
    if request.user.is_authenticated:
        # Unified dashboard for all roles
        return redirect('owner_dashboard')
    return redirect('login')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Authenticate using email as username
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
