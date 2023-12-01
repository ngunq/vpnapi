import logging

from django.conf import settings

from .runner import AnsibleRunner

logger = logging.getLogger('ansible')


class ProxmoxCreateTemplate(AnsibleRunner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__name__ = 'proxmox_create_template'
        self.playbook_path = str(settings.BASE_DIR) + '/api/ansible_helpers/Ansible/proxmox/proxmoxCreateTemplate.yaml'

        self.vmid = kwargs.get('vm_id')
        self.vmname = kwargs.get('vm_name')
        self.vmmemory = kwargs.get('vm_memory')
        self.vmbridge = kwargs.get('vm_bridge')
        self.vmstorage = kwargs.get('vm_disk')
        self.imageurl = kwargs.get('image_url')
        self.imagename = kwargs.get('image_name')

    def run(self):
        self.extra_vars = {
            'ansible_ssh_pass': self.password,
            'ansible_sudo_pass': self.password,

            'vmid': self.vmid,
            'vmname': self.vmname,
            'vmmemory': self.vmmemory,
            'vmbridge': self.vmbridge,
            'vmstorage': self.vmstorage,
            'imageurl': self.imageurl,
            'imagename': self.imagename
        }
        logger.info(f'running proxmox create template with: {self.extra_vars}')
        res = super().run()
        return res.get('msg', {}).get('success')
