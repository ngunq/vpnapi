import os


def upload_ovpn(instance, filename):
    _, name = os.path.split(filename)
    return f'openvpn/{instance.ip}/{name}'


def upload_wireguard(instance, filename):
    _, name = os.path.split(filename)

    return f'wireguard/{instance.server_vpn.ip}/{instance.client.username}/{name}'
