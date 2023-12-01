from django.db import models


class VPNType(models.IntegerChoices):
    OPENVPN = 1
    WIREGUARD = 2
