# get_public_server_vpn_clients,
# update_public_server_vpn_client, delete_public_server_vpn_client)
from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views import (get_public_server_vpns, setup_public_server_vpn_openvpn, setup_public_server_vpn_wireguard,
                       delete_public_server_vpn, public_server_vpn_wireguard_add_client, get_public_server_vpn_by_id,
                       get_public_server_vpn_openvpn_config, PublicServerClientsViewSet,
                       public_server_vpn_wireguard_remove_client)

public_server_vpn_urlpatterns = [
    path('PublicServersVPN/GetAll', get_public_server_vpns),
    path('PublicServersVPN/GetById', get_public_server_vpn_by_id),
    path('PublicServersVPN/SetupOpenvpn', setup_public_server_vpn_openvpn),
    path('PublicServersVPN/SetupWireguard', setup_public_server_vpn_wireguard),
    path('PublicServersVPN/Delete', delete_public_server_vpn),
    path('PublicServersVPN/WireguardAddClient', public_server_vpn_wireguard_add_client),
    path('PublicServersVPN/WireguardRemoveClient', public_server_vpn_wireguard_remove_client),
    path('PublicServersVPN/GetOpenVPNConfig', get_public_server_vpn_openvpn_config),
    # path('PublicServersVPN/GetClientConfig', get_public_server_vpn_openvpn_config),

    # path('PublicServersVPNUsers/GetAll', get_public_server_vpn_clients),
    # path('PublicServersVPNUsers/Update', update_public_server_vpn_client),
    # path('PublicServersVPNUsers/Delete', delete_public_server_vpn_client),
]

router = DefaultRouter()
router.register(r'PublicServersVpnClients', PublicServerClientsViewSet, basename='PublicServersVpnClient')

public_server_vpn_urlpatterns += router.urls
