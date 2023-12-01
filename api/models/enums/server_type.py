import enum
from django.db import models

class ServerType(str, enum.Enum):
    PRIVATE = 'private'
    PUBLIC = 'public'
    PRIVATE_VM = 'private_vm'

class ApiServerType(models.IntegerChoices):
    PRIVATE = 1
    PUBLIC = 2
    PRIVATE_VM = 3
