from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views import (get_private_server_vpns, delete_private_server_vpn,
                       get_private_server_vpn_by_id, private_server_vpn_wireguard_add_client,
                       setup_private_server_vpn_openvpn, setup_private_server_vpn_wireguard,
                       get_private_server_vpn_openvpn_config, private_server_vpn_wireguard_remove_client, PrivateServerClientsViewSet)

private_server_vpn_urlpatterns = [
    path('PrivateServersVPN/GetAll', get_private_server_vpns),
    path('PrivateServersVPN/GetById', get_private_server_vpn_by_id),
    path('PrivateServersVPN/SetupOpenvpn', setup_private_server_vpn_openvpn),
    path('PrivateServersVPN/SetupWireguard', setup_private_server_vpn_wireguard),
    path('PrivateServersVPN/Delete', delete_private_server_vpn),
    path('PrivateServersVPN/WireguardAddClient', private_server_vpn_wireguard_add_client),
    path('PrivateServersVPN/WireguardRemoveClient', private_server_vpn_wireguard_remove_client),
    path('PrivateServersVPN/GetOpenVPNConfig', get_private_server_vpn_openvpn_config),
]
router = DefaultRouter()
router.register(r'PrivateServersVpnClients', PrivateServerClientsViewSet, basename='PrivateServersVpnClient')

private_server_vpn_urlpatterns += router.urls