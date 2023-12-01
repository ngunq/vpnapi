import uuid
from datetime import datetime

from django.db import models


class PrivateServerVmOpenvpnSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column='Id')
    user = models.ForeignKey('api.AppUser', on_delete=models.CASCADE, db_column='UserId')
    server_vm = models.ForeignKey('api.PrivateServerVM', on_delete=models.CASCADE, db_column='ServerVMId')
    date = models.DateTimeField(default=datetime.now, editable=False, db_column='Datetime')

    @property
    def server(self):
        return self.server_vm

    class Meta:
        db_table = 'PrivateServerVMOpenvpnSessions'
