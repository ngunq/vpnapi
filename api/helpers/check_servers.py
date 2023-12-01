from icmplib import async_multiping


async def check_servers(ips):
    hosts = await async_multiping(ips)
    res = {}
    for host in hosts:
        res[host.address] = host.is_alive

    return res
