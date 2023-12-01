import logging

from celery import shared_task
from celery.result import AsyncResult

from api.ansible_helpers import ProxmoxStopVM
from api.models import PrivateServerVM
from api.tasks.utils import send_notification

logger = logging.getLogger('ansible')


@shared_task(bind=True, name='proxmox_stop_task')
def handle_proxmox_stop(self, vm_id):
    self.update_state(state='IN_PROGRESS')
    send_notification(f'proxmox stop task in progress for task {self.request.id}')
    obj = PrivateServerVM.objects.get(id=vm_id)
    proxmox_stop = ProxmoxStopVM(
        vmid=obj.vm_id,
        proxmox_node_name=obj.private_server.proxmox_node_name,
        host=obj.private_server.ip,
        username=obj.private_server.username,
        password=obj.private_server.password
    )
    try:
        ret = proxmox_stop.run()
        self.update_state(state='SUCCESS', meta={'message': 'Stopping Proxmox VM completed successfully'})
        send_notification(f'proxmox stop task done for task {self.request.id}')
    except Exception as e:
        logger.error(f'error stopping vm {e}')
        send_notification(f'proxmox stop task failed for task {self.request.id}')
        raise ValueError(f'Stopping Proxmox VM failed: {e}')