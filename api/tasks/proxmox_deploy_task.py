import logging
from random import randint
from celery import shared_task


from api.ansible_helpers import ProxmoxDeployVM
from api.models import PrivateServerVM, PrivateServerUser, AppUser
from api.tasks.utils import send_notification

logger = logging.getLogger('ansible')


@shared_task(bind=True, name='proxmox_deploy_task')
def handle_proxmox_deploy(self, obj_id, user_id):
    send_notification(f'starting vm deploy for task {self.request.id}')
    log_id = randint(111111, 888888)

    send_notification(f'starting vm deploy for task {self.request.id}')
    
    self.update_state(state='IN_PROGRESS')
    server_vm = PrivateServerVM.objects.get(id=obj_id)
    logger.info(f'{log_id} running proxmox task on {server_vm.id}')

    try:
        proxmox_deploy = ProxmoxDeployVM(
            **server_vm.__dict__,
            server_username=server_vm.private_server.username,
            server_password=server_vm.private_server.password,
            server_host=server_vm.private_server.ip,
            proxmox_default_disk=server_vm.private_server.proxmox_default_disk,
            proxmox_default_volume=server_vm.private_server.proxmox_default_volume,
            proxmox_node_name=server_vm.private_server.proxmox_node_name,
            proxmox_mask=server_vm.proxmox_ip.mask,
            proxmox_gateway=server_vm.proxmox_ip.gateway
        )
        res = proxmox_deploy.run()
    except Exception as e:
        logger.error(f'{log_id} Error deploying {e}')
        server_vm.proxmox_ip.is_reserved = False
        server_vm.proxmox_ip.save()
        server_vm.delete()
        send_notification(f'deployment failed for task {self.request.id} check status for details')
        self.update_state(state='FAILURE', meta={'message': 'Deployment failed', 'error_message': str(e)})
        raise ValueError(f'Deployment failed {e}')

    logger.info(f'{log_id} Proxmox Deploy Finished')
    server_vm.vm_id = res.get('vmid')
    server_vm.save()
    user = AppUser.objects.get(id=user_id)
    server_user = PrivateServerUser.objects.create(private_server=server_vm.private_server, user=user)
    server_user.save()
    logger.info(f'{log_id} Deploy success for server_vm {server_vm.id} and got vmid: {res.get("vmid")}')
    self.update_state(state='SUCCESS', meta={'message': 'Deployment completed successfully'})
    send_notification(f'Deployment completed successfully for {server_vm.id} and the vm_id is {server_vm.vm_id}')
    return {'id': server_vm.id}
