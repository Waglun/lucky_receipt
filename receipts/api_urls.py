from django.urls import path

from . import views

urlpatterns = [
    path("receipts/", views.receipts_api, name="receipts_api"),
]