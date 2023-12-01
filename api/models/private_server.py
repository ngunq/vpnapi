import uuid

from django.db import models
from django.db.models import Count

from .app_user import AppUser
from .provider import Provider


class PrivateServerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            consumed_ips=Count("privateservervm")
        )


class PrivateServer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column='Id')
    ip = models.GenericIPAddressField(protocol='IPv4', db_column='IP', null=True)
    username = models.CharField(max_length=100, db_column='username', null=True)
    password = models.CharField(max_length=1024, db_column='Password')
    city = models.CharField(max_length=100, db_column='City', null=True)
    country = models.CharField(max_length=100, db_column='Country', null=True)
    is_hardened = models.BooleanField(db_column='IsHardened', null=True)
    hostname = models.CharField(max_length=100, db_column='HostName', null=True)
    name = models.CharField(max_length=100, db_column='Name', null=True)
    status = models.BooleanField(db_column='Status', null=True)

    proxmox_default_volume = models.CharField(max_length=100, db_column='ProxmoxDefaultVolume', null=True)
    proxmox_node_name = models.CharField(max_length=100, db_column='ProxmoxNodeName', null=True)
    proxmox_default_disk = models.CharField(max_length=100, db_column='ProxmoxDefaultDisk', null=True)

    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, db_column='ProviderId', null=True)
    users = models.ManyToManyField(AppUser, through='PrivateServerUser')

    objects = PrivateServerManager()
    default_objects = models.Manager()
    class Meta:
        db_table = 'PrivateServers'

    def __str__(self) -> str:
        return str(self.name) + ' ' + str(self.id)


class PrivateServerUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column='Id')
    private_server = models.ForeignKey('api.PrivateServer', on_delete=models.CASCADE, db_column='PrivateServerId')
    user = models.ForeignKey('api.AppUser', on_delete=models.CASCADE, db_column='UserId')

    class Meta:
        db_table = 'PrivateServerUsers'
