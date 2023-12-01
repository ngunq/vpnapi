import logging

from celery import shared_task
from celery.result import AsyncResult

from api.ansible_helpers import ProxmoxStartVM
from api.models import PrivateServerVM
from api.tasks.utils import send_notification

logger = logging.getLogger('ansible')


@shared_task(bind=True, name='proxmox_start_task')
def handle_proxmox_start(self, vm_id):
    self.update_state(state='IN_PROGRESS')
    send_notification(f'proxmox start task in progress')
    obj = PrivateServerVM.objects.get(id=vm_id)
    proxmox_start = ProxmoxStartVM(
        vmid=obj.vm_id,
        proxmox_node_name=obj.private_server.proxmox_node_name,
        host=obj.private_server.ip,
        username=obj.private_server.username,
        password=obj.private_server.password
    )
    try:
        ret = proxmox_start.run()
        send_notification(f'proxmox start task done for {self.request.id}')
        self.update_state(state='SUCCESS', meta={'message': 'Starting Proxmox VM completed successfully'})
    except Exception as e:
        logger.error(f'error starting vm {e}')
        send_notification(f'proxmox start task failed for {self.request.id}')
        raise ValueError(f'Starting Proxmox VM failed: {e}')
