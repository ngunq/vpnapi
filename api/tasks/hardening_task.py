import logging
from random import randint
from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer

from django.conf import settings
from django.db import transaction

from api.ansible_helpers import Hardening
from .utils import get_server, send_notification

logger = logging.getLogger('ansible')


@shared_task(bind=True, name='hardening_task')
@transaction.atomic()
def handle_hardening(self, server_id, server_type, **kwargs):    
    log_id = randint(111111, 888888)
    try:        
        send_notification(f'starting hardening on {server_id}')
        self.update_state(state='IN_PROGRESS', meta={'message': 'Hardening in progress'})        
        server = get_server(server_id, server_type)
        logger.info(f'{log_id} starting hardening on {server.name} type  {server_type}  with ID {server_id}')
        hardener = Hardening(**kwargs)
        uuid = hardener.run()
        server.is_hardened = True
        server.hostname = str(uuid) + '.' + settings.DOMAIN
        server.save()
        self.update_state(state='SUCCESS', meta={'message': 'Hardening completed successfully'})
        send_notification(f'hardening finisihed on {server.name}')
        logger.info(f'{log_id} hardening finisihed on {server.name}')
    except Exception as e:
        logger.error(f'{log_id} error hardening {e}')
        raise ValueError(f'hardening failed {e}')

