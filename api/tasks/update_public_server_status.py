import asyncio
import logging

from celery import shared_task

from api.helpers import check_servers
from api.models import PublicServer

logger = logging.getLogger('ping_service')


@shared_task(ignore_result=True)
def update_public_server_status():
    servers = PublicServer.objects.all()
    if len(servers) == 0:
        return
    ips = [server.ip for server in servers]
    res = asyncio.run(check_servers(ips))
    # logger.info(f'public servers ips result:\n {res}')
    for server in servers:
        logger.info(f'server {server.name} with ip {server.ip} new_status: {res[server.ip]}')
        server.status = res[server.ip]
        server.save(update_fields=['status'])
