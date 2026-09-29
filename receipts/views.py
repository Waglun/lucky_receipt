from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def register_receipt(request):
    return render(request, 'receipts/register.html')


@login_required
def cabinet(request):
    return render(request, 'receipts/cabinet.html')