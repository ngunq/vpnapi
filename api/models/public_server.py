import uuid

from django.db import models

from .app_user import AppUser
from .provider import Provider



class PublicServer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column='Id')
    ip = models.GenericIPAddressField(protocol='IPv4', db_column='IP', blank=True, null=True)
    username = models.CharField(max_length=100, db_column='username', null=True)
    password = models.CharField(max_length=1024, db_column='Password', null=True)
    city = models.CharField(max_length=100, db_column='City', null=True)
    country = models.CharField(max_length=100, db_column='Country', null=True)
    is_hardened = models.BooleanField(db_column='IsHardened', default=False)
    hostname = models.CharField(max_length=100, db_column='HostName', null=True, blank=True)
    name = models.CharField(max_length=100, db_column='Name', null=True)
    status = models.BooleanField(db_column='Status', null=True)
    
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, db_column='ProviderId', null=True)
    users = models.ManyToManyField(AppUser, db_table='PublicServerUsers', blank=True)

    class Meta:
        db_table = 'PublicServers'
