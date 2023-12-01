from django.urls import path

from api.views import (get_public_servers, update_public_server, delete_public_server, harden_public_server,
                       get_public_server_by_id)

public_server_urlpatterns = [
    # public servers
    path('PublicServers/GetAll', get_public_servers),
    path('PublicServers/GetById', get_public_server_by_id),
    path('PublicServers/Update', update_public_server),
    path('PublicServers/Delete', delete_public_server),
    # path('PublicServers/Provision', provision_public_server),
    # path('PublicServers/TestConnection', test_public_server_connection),
    # path('PublicServers/Connect', connect_to_public_server),
    path('PublicServers/Harden', harden_public_server),
]
