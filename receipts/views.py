from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .forms import ReceiptForm
from .models import Receipt


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
        {"form": form},
    )


@login_required
def cabinet(request):
    receipts = Receipt.objects.filter(
        user=request.user
    ).order_by("-purchase_datetime")

    paginator = Paginator(receipts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "receipts/cabinet.html",
        {
            "page_obj": page_obj,
        },
    )