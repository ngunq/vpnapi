from django.urls import path

from api.views import (get_private_server_vms, start_private_server_vm, stop_private_server_vm,
                       delete_private_server_vm, harden_private_server_vm, get_private_server_vm_by_id,
                       get_private_server_vm_users,
                       create_private_server_vm_user, update_private_server_vm_user, delete_private_server_vm_user,
                       deploy_private_server_vm)

private_server_vm_urlpatterns = [
    path('PrivateServersVM/GetAll', get_private_server_vms),
    path('PrivateServersVM/GetById', get_private_server_vm_by_id),
    # path('PrivateServersVM/Update', update_private_server_vm),
    path('PrivateServersVM/Delete', delete_private_server_vm),
    path('PrivateServersVM/Harden', harden_private_server_vm),
    path('PrivateServersVM/Deploy', deploy_private_server_vm),
    path('PrivateServersVM/Start', start_private_server_vm),
    path('PrivateServersVM/Stop', stop_private_server_vm),

    # Private Servers VM Users
    path('PrivateServersVMUsers/CreatePrivateServerVmUser', create_private_server_vm_user),
    path('PrivateServersVMUsers/GetAll', get_private_server_vm_users),
    path('PrivateServersVMUsers/Update', update_private_server_vm_user),
    path('PrivateServersVMUsers/Delete', delete_private_server_vm_user),
]
