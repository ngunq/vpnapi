import uuid

from django.db import models


class MgmtWhitelistedIp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column='Id')
    name = models.CharField(max_length=50, db_column='Name', null=True)
    ip = models.GenericIPAddressField(protocol='IPv4', db_column='IP', null=True)

    class Meta:
        db_table = 'MgmtWhitelistedIp'
