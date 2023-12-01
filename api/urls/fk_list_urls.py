from django.urls import path

from api.views import get_provider_fks, get_public_server_fks, get_private_server_fks, get_private_server_vm_fks, \
    get_usernames

fk_list_urlpatterns = [
    path('ForeignKeysList/Provider', get_provider_fks),
    path('ForeignKeysList/PublicServer', get_public_server_fks),
    path('ForeignKeysList/PrivateServer', get_private_server_fks),
    path('ForeignKeysList/PrivateServerVM', get_private_server_vm_fks),
    path('ForeignKeysList/Usernames', get_usernames),
]