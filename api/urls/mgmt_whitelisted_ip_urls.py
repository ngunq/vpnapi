from django.urls import path

from api.views import get_mgmt_whitelisted_ips, delete_mgmt_whitelisted_ip, update_mgmt_whitelisted_ip, \
    get_mgmt_whitelisted_ip_by_id

mgmt_whitelisted_ip_urlpatterns = [
    path('MgmtWhitelistedIp/GetAll', get_mgmt_whitelisted_ips),
    path('MgmtWhitelistedIp/GetById', get_mgmt_whitelisted_ip_by_id),
    path('MgmtWhitelistedIp/Update', update_mgmt_whitelisted_ip),
    path('MgmtWhitelistedIp/Delete', delete_mgmt_whitelisted_ip),
]