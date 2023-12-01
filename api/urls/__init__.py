from .account_urls import account_urlpatterns
from .client_urls import client_urlpatterns
from .dashboard_urls import dashboard_urlpatterns
from .enums_urls import enum_urlpatterns
from .fk_list_urls import fk_list_urlpatterns
from .mgmt_whitelisted_ip_urls import mgmt_whitelisted_ip_urlpatterns
from .openvpn_urls import openvpn_urlpatterns
from .private_server_urls import private_server_urlpatterns
from .private_server_vm_urls import private_server_vm_urlpatterns
from .private_server_vpn_urls import private_server_vpn_urlpatterns
from .provider_urls import provider_urlpatterns
from .proxmox_subnet_urls import proxmox_subnet_urlpatterns
from .public_server_urls import public_server_urlpatterns
from .public_server_vpn_urls import public_server_vpn_urlpatterns
from .celery_urls import celery_urlpatterns
from .servers_util_urls import server_util_urls

urlpatterns = []
urlpatterns += account_urlpatterns
urlpatterns += private_server_urlpatterns
urlpatterns += public_server_urlpatterns
urlpatterns += provider_urlpatterns
urlpatterns += mgmt_whitelisted_ip_urlpatterns
urlpatterns += enum_urlpatterns
urlpatterns += fk_list_urlpatterns
urlpatterns += openvpn_urlpatterns
urlpatterns += private_server_vm_urlpatterns
urlpatterns += private_server_vpn_urlpatterns
urlpatterns += public_server_vpn_urlpatterns
urlpatterns += proxmox_subnet_urlpatterns
urlpatterns += client_urlpatterns
urlpatterns += dashboard_urlpatterns
urlpatterns += celery_urlpatterns
urlpatterns += server_util_urls
