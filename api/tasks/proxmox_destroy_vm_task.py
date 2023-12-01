import logging

from celery import shared_task
from celery.result import AsyncResult
from django.db import transaction

from api.ansible_helpers import ProxmoxDestroyVM
from api.helpers.cloudflare import delete_cloudflare_dns
from api.models import PrivateServerVM
from api.tasks.utils import send_notification

logger = logging.getLogger('ansible')


@shared_task(bind=True, name='proxmox_destroy_vm_task')
@transaction.atomic()
def handle_vm_destroy(self, obj_id):
    send_notification(f'starting destroy vm for task {self.request.id}')
    self.update_state(state='IN_PROGRESS')

    obj = PrivateServerVM.objects.get(id=obj_id)

    if obj.is_hardened:
        try:
            hostname = obj.hostname
            delete_cloudflare_dns(hostname)
        except Exception as e:
            logger.error(f'error deleting dns vm {e}')
        
    proxmox_destroy = ProxmoxDestroyVM(
        vmid=obj.vm_id,
        proxmox_node_name=obj.private_server.proxmox_node_name,
        host=obj.private_server.ip,
        username=obj.private_server.username,
        password=obj.private_server.password
    )
    try:
        ret = proxmox_destroy.run()
    except Exception as e:
        logger.error(f'error destroying vm {e}')
        send_notification('destroy vm failed check status for details')
        raise ValueError(f'Proxmox Destroy VM failed {e}')

    for session in obj.privateservervmopenvpnsession_set.all():
        if session.user.openvpn_sessions > 0:
            session.user.openvpn_sessions -= 1
            session.user.save()

    for vpn in obj.privateservervpn_set.all():
        for client in vpn.wireguard_clients.all():
            if client.wireguard_sessions > 0:
                client.wireguard_sessions -= 1
                client.save()

    if obj.proxmox_ip is not None:
        obj.proxmox_ip.is_reserved = False
        obj.proxmox_ip.save()

    obj.save()
    obj.delete()
    logger.info(f'destroy success {ret}')
    send_notification(f'Proxmox Destroy VM completed successfully for task {self.request.id}')
    self.update_state(state='SUCCESS', meta={'message': 'Proxmox Destroy VM completed successfully'})
