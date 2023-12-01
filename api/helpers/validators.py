import ipaddress

from django.core.exceptions import ValidationError


def validate_subnet(value :str):
    try:
        ipaddress.IPv4Network(value)
    except:
        raise ValidationError('%(value)s is not a valid subnet', params={'value': value})
