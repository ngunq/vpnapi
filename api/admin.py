from django.contrib import admin

from api.models import (PrivateServer, PrivateServerVM, PrivateServerVPN, PublicServer,
                        PublicServerVPN, Provider, AppUser, MgmtWhitelistedIp, ProxmoxIP,
                        PrivateServerVpnWireguardClient, PublicServerVpnWireguardClient,
                        PrivateServerVmOpenvpnSession, PublicServerOpenvpnSession)

# Register your models here.

admin.site.register(AppUser)
admin.site.register(PublicServerVPN)
admin.site.register(PublicServer)
admin.site.register(PrivateServerVM)
admin.site.register(PrivateServerVPN)
admin.site.register(PrivateServer)
admin.site.register(Provider)
admin.site.register(MgmtWhitelistedIp)
admin.site.register(ProxmoxIP)
admin.site.register(PrivateServerVpnWireguardClient)
admin.site.register(PublicServerVpnWireguardClient)
admin.site.register(PrivateServerVmOpenvpnSession)
admin.site.register(PublicServerOpenvpnSession)
