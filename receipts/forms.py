from decimal import Decimal

from django import forms
from django.conf import settings

from .models import Receipt


class ReceiptForm(forms.ModelForm):
    purchase_datetime = forms.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            format="%Y-%m-%dT%H:%M",
            attrs={
                "type": "datetime-local",
            },
        ),
    )

    class Meta:
        model = Receipt
        fields = [
            "fn",
            "fd",
            "fp",
            "purchase_datetime",
            "amount",
        ]
        widgets = {
            "fn": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "id": "fn",
                    "placeholder": "Введите ФН",
                    "autocomplete": "off",
                }
            ),
            "fd": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "id": "check-number",
                    "placeholder": "Введите номер чека (ФД)",
                    "autocomplete": "off",
                }
            ),
            "fp": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "id": "fp",
                    "placeholder": "Введите ФП",
                    "autocomplete": "off",
                }
            ),
            "purchase_datetime": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={
                    "class": "form-input",
                    "id": "purchase-date",
                    "type": "datetime-local",
                },
            ),
            "amount": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "id": "amount",
                    "placeholder": "0.00 ₽",
                    "autocomplete": "off",
                }
            ),
        }

    def clean_fn(self):
        fn = self.cleaned_data["fn"]

        if not fn.isdigit():
            raise forms.ValidationError(
                "ФН должен содержать только цифры."
            )

        return fn

    def clean_fd(self):
        fd = self.cleaned_data["fd"]

        if not fd.isdigit():
            raise forms.ValidationError(
                "ФД должен содержать только цифры."
            )

        return fd

    def clean_fp(self):
        fp = self.cleaned_data["fp"]

        if not fp.isdigit():
            raise forms.ValidationError(
                "ФП должен содержать только цифры."
            )

        return fp

    def clean_amount(self):
        amount = self.cleaned_data["amount"]

        if amount < Decimal("1000"):
            raise forms.ValidationError(
                "Сумма чека должна быть не меньше 1000 ₽."
            )

        return amount

    def clean_purchase_datetime(self):
        purchase_datetime = self.cleaned_data["purchase_datetime"]

        purchase_date = purchase_datetime.date()

        if not (
                settings.PROMO_START_DATE
                <= purchase_date
                <= settings.PROMO_END_DATE
        ):
            raise forms.ValidationError(
                "Дата покупки не входит в период акции."
            )

        return purchase_datetime

    def clean(self):
        cleaned_data = super().clean()

        fn = cleaned_data.get("fn")
        fd = cleaned_data.get("fd")
        fp = cleaned_data.get("fp")

        if fn and fd and fp:
            if Receipt.objects.filter(
                    fn=fn,
                    fd=fd,
                    fp=fp,
            ).exists():
                raise forms.ValidationError(
                    "Этот чек уже зарегистрирован."
                )

        return cleaned_data