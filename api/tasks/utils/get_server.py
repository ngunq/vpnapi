from api.models import PrivateServer, PublicServer, PrivateServerVM
from api.models.enums import ServerType


def get_server(server_id, server_type):
    if server_type == ServerType.PRIVATE:
        return PrivateServer.objects.get(id=server_id)
    elif server_type == ServerType.PUBLIC:
        return PublicServer.objects.get(id=server_id)
    else:
        return PrivateServerVM.objects.get(id=server_id)
