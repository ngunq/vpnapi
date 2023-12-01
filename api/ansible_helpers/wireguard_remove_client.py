import logging
import os

from django.conf import settings

from .runner import AnsibleRunner

logger = logging.getLogger('ansible')


class WireguardRemoveClient(AnsibleRunner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__name__ = 'wireguard_remove_client'
        self.playbook_path = str(os.path.join(str(settings.BASE_DIR), 'api', 'ansible_helpers', 'Ansible', 'wireguard',
                                              'wireguardRemoveClient.yaml'))
        self.clientusername = kwargs.get('client_username')
        self.wireguard_interface = kwargs.get('interface_name')

    def run(self):
        self.extra_vars = {
            'ansible_ssh_pass': self.password,
            'ansible_sudo_pass': self.password,
            'username': self.clientusername,
            'wireguard_interface': self.wireguard_interface
        }
        logger.info(f'running wireguard remove client with: {self.extra_vars}')

        res = super().run()

        return res
