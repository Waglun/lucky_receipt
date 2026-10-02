from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('receipts/', include('receipts.urls')),
    path("api/", include("receipts.api_urls")),
]
