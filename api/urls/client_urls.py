from django.urls import path

from api.views import get_client_private_vm

client_urlpatterns = [
    path('Client/GetPrivateVM', get_client_private_vm)
]
