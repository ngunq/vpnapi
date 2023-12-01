from django.urls import path

from api.views import get_vpn_types, get_transports, get_user_types

enum_urlpatterns = [
    path('Enums/VPN', get_vpn_types),
    path('Enums/Transport', get_transports),
    path('Enums/UserType', get_user_types),
]