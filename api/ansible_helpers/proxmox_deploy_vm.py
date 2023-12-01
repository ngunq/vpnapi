import logging

from django.conf import settings

from api.utils.crypto import decrypt

from .runner import AnsibleRunner

logger = logging.getLogger('ansible')


class ProxmoxDeployVM(AnsibleRunner):
    def __init__(self, **kwargs):
        super().__init__(username=kwargs.get('server_username'), password=kwargs.get('server_password'),
                         host=kwargs.get('server_host'))
        self.__name__ = 'proxmox_deploy_vm'
        self.playbook_path = str(settings.BASE_DIR) + '/api/ansible_helpers/Ansible/proxmox/proxmoxDeployVM.yaml'
        self.node_name = kwargs.get('proxmox_node_name')  # proxmoxnodename

        self.api_user = self.username
        self.api_password = self.password
        self.api_host = self.node_name

        self.default_disk = kwargs.get('proxmox_default_disk')  # proxmoxdefaultdisk
        self.default_volume = kwargs.get('proxmox_default_volume')  # proxmoxdefaultvolume

        self.vm_sockets = kwargs.get('vm_socket')
        self.vm_cores = kwargs.get('vm_cores')
        self.vm_memory = kwargs.get('vm_memory')
        self.vm_disk = kwargs.get('vm_disk')
        self.vmbridge = kwargs.get('vm_bridge')
        self.vm_name = kwargs.get('vm_name')  # vmname
        self.vm_ip = kwargs.get('ip')  # proxmoxsubnets( choose an ip)
        self.vm_netmask = kwargs.get('proxmox_mask')  # proxmoxsubnetmask
        self.vm_gateway = kwargs.get('proxmox_gateway')  # proxmoxgateway
        self.root_password = decrypt(kwargs.get('password'))  # generate pass and save it in privateservervm password
        self.vm_template = "VM9000"

    def run(self):
        self.extra_vars = {
            'ansible_ssh_pass': self.password,
            'ansible_sudo_pass': self.password,
            'api_user': self.api_user + '@pam',
            'api_password': self.api_password,
            'api_host': self.api_host,
            'default_disk': self.default_disk,
            'default_volume': self.default_volume,
            'vm_sockets': self.vm_sockets,
            'vm_cores': self.vm_cores,
            'vm_memory': self.vm_memory,
            'vmbridge': self.vmbridge,
            'vm_name': self.vm_name,
            'node_name': self.node_name,
            'vm_template': self.vm_template,
            'vm_disk': self.vm_disk,
            'vm_ip': self.vm_ip,
            'vm_netmask': self.vm_netmask,
            'vm_gateway': self.vm_gateway,
            'root_password': self.root_password
        }
        logger.info(f'running proxmox deploy vm with: {self.extra_vars}')
        res = super().run()
        logger.info(f'proxmox deploy result: {res}')
        return res.get('msg', {'vmid': -1})
