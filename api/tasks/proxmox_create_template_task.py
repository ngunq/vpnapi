import logging

from celery import shared_task
from celery.result import AsyncResult

from api.ansible_helpers import ProxmoxCreateTemplate

logger = logging.getLogger('ansible')


@shared_task(bind=True, name='proxmox_create_template_task')
def handle_create_template(self, **kwargs):    
    try:
        self.update_state(state='IN_PROGRESS')
        proxmox_create = ProxmoxCreateTemplate(**kwargs)
        proxmox_create.run()
        self.update_state(state='SUCCESS', meta={'message': 'Proxmox Create Template completed successfully'})
    except Exception as e:
        logger.error(f'create template failed {e}')
        self.update_state(state='FAILURE', meta={'message': 'Proxmox Create Template failed', 'error_message': str(e)})
        raise ValueError(f'Proxmox Create Template failed {e}')