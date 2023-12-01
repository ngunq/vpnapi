from ipaddress import IPv4Network, IPv4Address


def get_valid_ip(server):
    ip = server.proxmoxip_set.filter(is_reserved=False, is_disabled=False).order_by('ip').first()
    return ip


def get_ip_range(start, end):
    start = IPv4Address(start)
    end = IPv4Address(end)
    res = []
    while start <= end:
        res.append(str(start))
        start += 1
    return res


def get_total_ips(subnet) -> int:
    network = IPv4Network(subnet.proxmox_subnet + '/' + str(subnet.proxmox_mask))
    return network.num_addresses
