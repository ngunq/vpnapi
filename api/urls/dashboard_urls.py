from django.urls import path

from api.views import (count_public_servers, count_private_servers, count_private_server_vms,
                       count_open_vpn_public_sessions, count_open_vpn_private_sessions,
                       open_vpn_sessions_by_public_server, open_vpn_sessions_by_private_server_vm,
                       count_public_end_users, count_private_end_users, private_server_stats
                       )

dashboard_urlpatterns = [
    path('Dashboard/CountPublicServers', count_public_servers),
    path('Dashboard/CountPrivateServers', count_private_servers),
    path('Dashboard/CountPrivateServerVMs', count_private_server_vms),
    path('Dashboard/CountOpenVpnPublicSessions', count_open_vpn_public_sessions),
    path('Dashboard/CountOpenVpnPrivateSessions', count_open_vpn_private_sessions),
    path('Dashboard/OpenVpnSessionsByPublicServer', open_vpn_sessions_by_public_server),
    path('Dashboard/OpenVpnSessionsByPrivateServerVm', open_vpn_sessions_by_private_server_vm),
    path('Dashboard/CountPublicEndUsers', count_public_end_users),
    path('Dashboard/CountPrivateEndUsers', count_private_end_users),
    path('Dashboard/PrivateServerStats', private_server_stats),
]
