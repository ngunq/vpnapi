import uuid

from django.db import models

# from . import ProxmoxIP
from .private_server import PrivateServer


class PrivateServerVM(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column='Id')
    name = models.CharField(max_length=50, db_column='Name', null=True)
    ip = models.GenericIPAddressField(protocol='IPv4', db_column='IP', null=True)
    username = models.CharField(max_length=50, db_column='Username', null=True, default='root')
    password = models.CharField(max_length=1024, db_column='Password', null=True)
    is_hardened = models.BooleanField(db_column='IsHardened', default=False)
    hostname = models.CharField(max_length=100, db_column='HostName', null=True)
    status = models.BooleanField(db_column='Status', null=True)
    is_enabled = models.BooleanField(db_column='isEnabled', default=True)

    vm_name = models.CharField(max_length=50, db_column='VmName', null=True)
    vm_id = models.IntegerField(db_column='VmId', null=True)
    vm_socket = models.IntegerField(db_column='VmSocket', null=True)
    vm_cores = models.IntegerField(db_column='VmCores', null=True)
    vm_memory = models.IntegerField(db_column='VmMemory', null=True)
    vm_bridge = models.CharField(max_length=100, db_column='VmBridge', null=True)
    vm_disk = models.IntegerField(db_column='VmDisk', null=True)
    vm_template = models.CharField(max_length=100, db_column='VmTemplate', null=True)
    private_server = models.ForeignKey(PrivateServer, on_delete=models.CASCADE, db_column='PrivateServerId')
    proxmox_ip = models.ForeignKey('api.ProxmoxIP', on_delete=models.CASCADE, db_column='ProxmoxIP', null=True)

    class Meta:
        db_table = 'PrivateServersVM'

    def __str__(self) -> str:
        return self.name
