from django.urls import path

from api.views import open_vpn_login, open_vpn_connect, open_vpn_disconnect, get_private_server_vm_sessions, \
    get_public_server_sessions, kill_public_server_sessions, kill_private_server_sessions, get_user_public_sessions, \
    get_user_private_sessions

openvpn_urlpatterns = [
    path('OpenVPN/Login', open_vpn_login),
    path('OpenVPN/connect', open_vpn_connect),
    path('OpenVPN/disconnect', open_vpn_disconnect),
    path('OpenVPN/GetPublicSessions', get_public_server_sessions),
    path('OpenVPN/GetPrivateSessions', get_private_server_vm_sessions),
    path('OpenVPN/KillPublicSession', kill_public_server_sessions),
    path('OpenVPN/KillPrivateSession', kill_private_server_sessions),
    path('OpenVPN/GetUserPublicSessions', get_user_public_sessions),
    path('OpenVPN/GetUserPrivateSessions', get_user_private_sessions),
]
