from django.urls import path

from . import views

app_name = 'receipts'

urlpatterns = [
    path("register/", views.register_receipt, name="register_receipt"),
    path("cabinet/", views.cabinet, name="cabinet"),
]