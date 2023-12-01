import os
import uuid

from django.db import models

from api.helpers import upload_ovpn, upload_wireguard
from .enums import Transport, VPNType
from .private_server_vm import PrivateServerVM


class PrivateServerVPN(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column='Id')
    port = models.IntegerField(db_column='Port', null=True)
    status = models.BooleanField(db_column='Status', null=True)
    # config = models.FileField(upload_to=upload_ovpn, db_column='Config', null=True, max_length=200)
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

    private_server_vm: PrivateServerVM = models.ForeignKey(PrivateServerVM, on_delete=models.CASCADE,
                                                           db_column='PrivateServerVMId')
    wireguard_clients = models.ManyToManyField('api.AppUser', through='api.PrivateServerVpnWireguardClient')

    @property
    def hostname(self):
        return self.private_server_vm.hostname

    @property
    def ip(self):
        return self.private_server_vm.ip

    class Meta:
        db_table = 'PrivateServersVPNs'

    # def delete(self, using=None, keep_parents=False):
    #     conf_path = os.path.dirname(self.config.path) if self.config else None
    #     if self.config:
    #         self.config.delete()
    #     super().delete(using=using, keep_parents=keep_parents)
    #     try:
    #         os.removedirs(conf_path)
    #     except:
    #         pass


class PrivateServerVpnWireguardClient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column='Id')
    private_server_vpn = models.ForeignKey('api.PrivateServerVPN', on_delete=models.CASCADE,
                                           db_column='PrivateServerVpnId')
    client = models.ForeignKey('api.AppUser', on_delete=models.CASCADE, db_column='Client')
    # config = models.FileField(upload_to=upload_wireguard, db_column='Config', null=True)
    config = models.TextField(db_column='Config', null=True)
    # qr_file = models.FileField(upload_to=upload_wireguard, db_column='QrFile', null=True)
    qr_file = models.TextField(db_column='QrFile', null=True)

    @property
    def server_vpn(self):
        return self.private_server_vpn

    class Meta:
        db_table = 'PrivateServerVpnWireguardClients'

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
