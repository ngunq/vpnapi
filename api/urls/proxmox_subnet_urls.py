from django.urls import path

from api.views import get_proxmox_subnets, get_proxmox_subnet_by_id, delete_proxmox_subnet, create_proxmox_ips, \
    disable_proxmox_ip

proxmox_subnet_urlpatterns = [
    path('ProxmoxSubnet/GetAll', get_proxmox_subnets),
    path('ProxmoxSubnet/GetById', get_proxmox_subnet_by_id),
    path('ProxmoxSubnet/Create', create_proxmox_ips),
    path('ProxmoxSubnet/Delete', delete_proxmox_subnet),
    path('ProxmoxSubnet/Disable', disable_proxmox_ip),
]
