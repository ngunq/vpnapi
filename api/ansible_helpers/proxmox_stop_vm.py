import logging

from django.conf import settings

from .runner import AnsibleRunner

logger = logging.getLogger('ansible')


class ProxmoxStopVM(AnsibleRunner):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__name__ = 'proxmox_Stop_vm'
        self.playbook_path = str(settings.BASE_DIR) + '/api/ansible_helpers/Ansible/proxmox/proxmoxStopVM.yaml'
        self.vm_id = kwargs.get('vmid')

    def run(self):
        self.extra_vars = {
            'ansible_ssh_pass': self.password,
            'ansible_sudo_pass': self.password,
            'vm_id': self.vm_id
        }
        logger.info(f'running proxmox Stop vm with: {self.extra_vars}')
        res = super().run()
        return res.get('msg', {}).get('success')
