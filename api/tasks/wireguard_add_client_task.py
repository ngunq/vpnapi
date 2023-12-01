from celery import shared_task
from django.core.files import File

from api.ansible_helpers import WireguardAddClient
from api.models import AppUser
from .utils import get_vpn_client, send_notification
import logging

logger = logging.getLogger('ansible')


@shared_task(bind=True, name='wireguard add client task')
def handle_wireguard_add_client(self, vpn_id, vpn_server_type, user_id, **kwargs):
    send_notification(f'wireguard add client task in progress for task {self.request.id}')
    self.update_state(state='IN_PROGRESS')
    logger.info(f'Adding Wireguard Client')
    user = AppUser.objects.get(id=user_id)
    instance = get_vpn_client(vpn_id, vpn_server_type)
    wireguard_add = WireguardAddClient(**kwargs)
    try:
        res = wireguard_add.run()
    except Exception as e:
        logger.error(f'failed to add wireguard {e}')
        instance.delete()
        send_notification(f'wireguard add client task failed for task {self.request.id}')
        raise ValueError(f'Adding Wireguard client failed: {e}')

    instance.config = res.get('client_config_text')
    instance.qr_file = res.get('client_qr_code_base64')
    instance.save()
    user.wireguard_sessions += 1
    user.save()
    self.update_state(state='SUCCESS', meta={'message': 'Adding Wireguard client completed successfully'})
    logger.info(f'Adding Wireguard client completed successfully')
    send_notification(f'wireguard add client task done for task {self.request.id}')
    return {'id': str(instance.id)}
