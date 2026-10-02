from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.conf import settings

from .forms import ReceiptForm
from .models import Receipt
from django.http import JsonResponse


@login_required
def register_receipt(request):
    if request.method == "POST":
        form = ReceiptForm(request.POST)

        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.user = request.user
            receipt.status = Receipt.Status.PENDING
            receipt.save()

            return redirect("receipts:cabinet")

    else:
        form = ReceiptForm()

    return render(
        request,
        "receipts/register.html",
        {
            "form": form,
            "promo_start_date": settings.PROMO_START_DATE,
            "promo_end_date": settings.PROMO_END_DATE,
        },
    )


@login_required
def cabinet(request):
    receipts = Receipt.objects.filter(
        user=request.user
    ).order_by("-registered_at")

    paginator = Paginator(receipts, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "receipts/cabinet.html",
        {
            "receipts": page_obj,
        },
    )


@login_required
def receipts_api(request):
    receipts = Receipt.objects.filter(
        user=request.user
    ).order_by("-purchase_datetime")

    data = []

    for receipt in receipts:
        data.append({
            "id": receipt.id,
            "fn": receipt.fn,
            "fd": receipt.fd,
            "fp": receipt.fp,
            "purchase_datetime": receipt.purchase_datetime.isoformat(),
            "amount": str(receipt.amount),
            "status": receipt.status,
            "rejection_reason": receipt.rejection_reason,
            "registered_at": receipt.registered_at.isoformat(),
        })

    return JsonResponse(data, safe=False)