from django.urls import path

from api.views import (get_private_servers, update_private_server, delete_private_server, harden_private_server,
                       get_private_server_by_id, get_private_server_users,
                       update_private_server_user, delete_private_server_user, get_ip, create_template)

private_server_urlpatterns = [
    # private servers
    path('PrivateServers/GetAll', get_private_servers),
    path('PrivateServers/GetById', get_private_server_by_id),
    path('PrivateServers/Update', update_private_server),
    path('PrivateServers/Delete', delete_private_server),
    # path('PrivateServers/Provision', provision_private_server),
    # path('PrivateServers/TestConnection', test_private_server_connection),
    # path('PrivateServers/Connect', connect_to_private_server),
    path('PrivateServers/Harden', harden_private_server),
    path('PrivateServers/CreateTemplate', create_template),
    path('PrivateServers/GetIp', get_ip),

    # private server users
    path('PrivateServerUsers/GetAll', get_private_server_users),
    path('PrivateServerUsers/Update', update_private_server_user),
    path('PrivateServerUsers/Delete', delete_private_server_user),
]
