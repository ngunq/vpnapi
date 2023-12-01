from django.db import models


class Transport(models.IntegerChoices):
    TCP = 1
    UDP = 2
