from api.models import PrivateServerVpnWireguardClient, PublicServerVpnWireguardClient
from api.models.enums import ServerType


def get_vpn_client(vpn_id, server_type):
    if server_type == ServerType.PRIVATE:
        return PrivateServerVpnWireguardClient.objects.get(id=vpn_id)
    elif server_type == ServerType.PUBLIC:
        return PublicServerVpnWireguardClient.objects.get(id=vpn_id)

