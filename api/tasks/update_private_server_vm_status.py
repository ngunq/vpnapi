import asyncio
import logging

from celery import shared_task

from api.helpers import check_servers
from api.models import PrivateServerVM

logger = logging.getLogger('ping_service')


@shared_task(ignore_result=True)
def update_private_server_vm_status():
    servers = PrivateServerVM.objects.all()
    if len(servers) == 0:
        return
    ips = [server.ip for server in servers]
    res = asyncio.run(check_servers(ips))
    # logger.info(f'private server vms ips result:\n {res}')
    for server in servers:
        logger.info(f'server_vm {server.name} with ip {server.ip} new_status: {res[server.ip]}')
        server.status = res[server.ip]
        server.save(update_fields=['status'])
