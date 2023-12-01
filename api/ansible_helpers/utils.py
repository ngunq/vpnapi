from ipaddress import IPv4Network


def get_mask(ip):
    network = IPv4Network(ip)
    return str(network.netmask)
