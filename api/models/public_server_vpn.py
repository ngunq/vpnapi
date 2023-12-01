import os
import uuid

from django.db import models

from api.helpers.upload_helpers import upload_ovpn, upload_wireguard
from .enums import Transport, VPNType
from .public_server import PublicServer


class PublicServerVPN(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column='Id')
    port = models.IntegerField(db_column='Port', null=True)
    status = models.BooleanField(db_column='Status', null=True)
    # config = models.FileField(upload_to=upload_ovpn, db_column='Config', null=True)
    config = models.TextField(db_column='Config', null=True)
    vpn_type = models.PositiveSmallIntegerField(choices=VPNType.choices, db_column='VpnType', null=True)
    transport = models.PositiveSmallIntegerField(choices=Transport.choices, db_column='Transport', null=True)
    private_subnet = models.CharField(max_length=50, db_column='PrivateSubnet', null=True)
    private_subnet_mask = models.IntegerField(db_column='PrivateSubnetMask', null=True)
    private_ip = models.GenericIPAddressField(protocol='IPv4', db_column='PrivateIP', null=True)
    private_key = models.CharField(max_length=100, db_column='PrivateKey', null=True)
    public_key = models.CharField(max_length=100, db_column='PublicKey', null=True)
    interface_name = models.CharField(max_length=100, db_column='InterfaceName', null=True)
    dns = models.CharField(max_length=100, db_column='dns', null=True)
    keep_alive = models.IntegerField(db_column='KeepAlive', null=True)

    public_server: PublicServer = models.ForeignKey(PublicServer, on_delete=models.CASCADE, db_column='ServerId')
    wireguard_clients = models.ManyToManyField('api.AppUser', through='api.PublicServerVpnWireguardClient')

    @property
    def hostname(self):
        return self.public_server.hostname

    @property
    def ip(self):
        return self.public_server.ip

    class Meta:
        db_table = 'PublicServersVPNs'

    # def delete(self, using=None, keep_parents=False):
    #     conf_path = os.path.dirname(self.config.path) if self.config else None
    #     if self.config:
    #         self.config.delete()
    #     super().delete(using=using, keep_parents=keep_parents)
    #     try:
    #         os.removedirs(conf_path)
    #     except:
    #         pass


class PublicServerVpnWireguardClient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column='Id')
    public_server_vpn = models.ForeignKey('api.PublicServerVPN', on_delete=models.CASCADE,
                                          db_column='PublicServerVpnId')
    client = models.ForeignKey('api.AppUser', on_delete=models.CASCADE, db_column='Client')
    config = models.TextField(db_column='Config', null=True)
    qr_file = models.TextField(db_column='QrFile', null=True)

    @property
    def server_vpn(self):
        return self.public_server_vpn

    class Meta:
        db_table = 'PublicServerVpnWireguardClients'

    # def delete(self, using=None, keep_parents=False):
    #     conf_path = os.path.dirname(self.config.path) if self.config else None
    #     if self.config:
    #         self.config.delete()
    #     if self.qr_file:
    #         self.qr_file.delete()
    #     super().delete(using=using, keep_parents=keep_parents)
    #     try:
    #         os.removedirs(conf_path)
    #     except:
    #         pass
