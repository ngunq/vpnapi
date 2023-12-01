import uuid

from django.db import models


class Provider(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column='Id')
    name = models.CharField(max_length=100, db_column='Name', null=True)

    class Meta:
        db_table = 'Providers'
        ordering = ['name']
