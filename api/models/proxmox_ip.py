import uuid

from django.db import models

from .private_server import PrivateServer


class ProxmoxIP(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column='Id')
    ip = models.GenericIPAddressField(protocol='IPv4', db_column='IP', null=True)
    gateway = models.CharField(max_length=50, db_column='Gateway', null=True)
    private_server = models.ForeignKey(PrivateServer, on_delete=models.CASCADE, db_column='PrivateServerId')
    is_disabled = models.BooleanField(default=False, db_column='IsDisabled')
    is_reserved = models.BooleanField(default=False, db_column='IsReserved')
    mask = models.IntegerField(db_column='ProxmoxMask', null=True)

    class Meta:
        db_table = 'ProxmoxIPs'
