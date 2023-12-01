from dj_rest_auth.views import (
    LogoutView, LoginView
)
from django.urls import path

from api.views import get_user_details, get_accounts, update_user, reset_password, update_account_status, \
    RegisterViewV2, delete_account, suspend_account, update_wireguard_session_limit, update_openvpn_session_limit

account_urlpatterns = [
    path('Account/Login', LoginView.as_view(), name='rest_login'),
    path('Account/Logout', LogoutView.as_view(), name='rest_logout'),
    path('Account/Register', RegisterViewV2.as_view(), name='rest_register'),
    path('Account/Get', get_user_details),
    path('Account/Update', update_user),
    path('Account/GetAll', get_accounts),
    path('Account/ResetPassword', reset_password),
    path('Account/UpdateRole', update_account_status),
    path('Account/Delete', delete_account),
    path('Account/Suspend', suspend_account),
    path('Account/UpdateOpenVPNSessionLimit', update_openvpn_session_limit),
    path('Account/UpdateWireguardSessionLimit', update_wireguard_session_limit),
]
