import uuid
from datetime import datetime

from django.db import models


class PublicServerOpenvpnSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column='Id')
    user = models.ForeignKey('api.AppUser', on_delete=models.CASCADE, db_column='UserId')
    server = models.ForeignKey('api.PublicServer', on_delete=models.CASCADE, db_column='ServerId')
    date = models.DateTimeField(default=datetime.now, editable=False, db_column='Datetime')

    class Meta:
        db_table = 'PublicServerOpenvpnSessions'
