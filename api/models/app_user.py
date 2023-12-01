import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserType(models.IntegerChoices):
    PRIVATE = 1
    PUBLIC = 2
    PRIVATE_SERVER_VM_USER = 3


class AppUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column='Id')
    user_type = models.PositiveSmallIntegerField(choices=UserType.choices, default=1, db_column='UserType')
    first_name = models.CharField("First Name", max_length=150, db_column='FirstName')
    last_name = models.CharField("Last Name", max_length=150, db_column='LastName')
    is_suspended = models.BooleanField(default=False, db_column='isSuspended')

    private_server_vm = models.ForeignKey('api.PrivateServerVM', on_delete=models.CASCADE, null=True)

    openvpn_sessions = models.PositiveIntegerField(default=0)
    openvpn_sessions_limit = models.PositiveIntegerField(default=settings.OPENVPN_SESSIONS_LIMIT)

    wireguard_sessions = models.PositiveIntegerField(default=0)
    wireguard_sessions_limit = models.PositiveIntegerField(default=settings.WIREGUARD_SESSIONS_LIMIT)

    class Meta:
        db_table = 'AppUsers'

    def __str__(self):
        return self.username + ' ' + str(self.id)
