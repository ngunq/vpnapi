import asyncio
import logging

from celery import shared_task

from api.helpers import check_servers
from api.models import PrivateServer

logger = logging.getLogger('ping_service')


@shared_task(ignore_result=True)
def update_private_server_status():
    servers = PrivateServer.objects.all()
    if len(servers) == 0:
        return
    ips = [server.ip for server in servers]
    res = asyncio.run(check_servers(ips))
    logger.info('running private server check')
    for server in servers:
        logger.info(f'server {server.name} with ip {server.ip} new_status: {res[server.ip]}')
        server.status = res[server.ip]
        server.save(update_fields=['status'])
