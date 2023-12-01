from celery import shared_task

from api.ansible_helpers import WireguardRemoveClient
from api.models import AppUser
from .utils import get_vpn_client, send_notification
import logging

logger = logging.getLogger('ansible')


@shared_task(bind=True, name='wireguard remove client task')
def handle_wireguard_remove_client(self, vpn_id, vpn_server_type, user_id, **kwargs):
    self.update_state(state='IN_PROGRESS')
    send_notification(f'wireguard remove client task in progress for task {self.request.id}')
    user = AppUser.objects.get(id=user_id)
    instance = get_vpn_client(vpn_id, vpn_server_type)
    wireguard_remove = WireguardRemoveClient(**kwargs)
    try:
        res = wireguard_remove.run()
        instance.delete()
        if user.wireguard_sessions > 0:
            user.wireguard_sessions -= 1
            user.save()
        self.update_state(state='SUCCESS', meta={'message': 'Wireguard remove client completed successfully'})
        send_notification(f'wireguard remove client task done for task {self.request.id}')
    except Exception as e:
        logger.error(f'{e}')
        send_notification(f'wireguard remove client task failed for task {self.request.id}')
        raise ValueError(f'Wireguard remove client failed: {e}')
