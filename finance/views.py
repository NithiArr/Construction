from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def expenses(request):
    return render(request, 'expenses.html')

@login_required
def purchases(request):
    return render(request, 'purchases.html')

@login_required
def payments(request):
    return render(request, 'payments.html')

@login_required
def client_payments(request):
    return render(request, 'client_payments.html')
