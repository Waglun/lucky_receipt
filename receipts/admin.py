from django.contrib import admin

from .models import Receipt


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = (
        "fn",
        "fd",
        "fp",
        "purchase_datetime",
        "amount",
        "status",
        "user",
        "registered_at",
    )

    list_filter = ("status",)

    search_fields = ("fn", "fd", "fp")