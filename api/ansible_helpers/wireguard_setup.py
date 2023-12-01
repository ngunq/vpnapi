import logging

from django.conf import settings

from .runner import AnsibleRunner

logger = logging.getLogger('ansible')


class WireguardSetup(AnsibleRunner):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__name__ = 'wireguard_setup'
        self.playbook_path = str(settings.BASE_DIR) + '/api/ansible_helpers/Ansible/wireguard/wireguardSetup.yaml'
        self.wireguard_port = kwargs.get('port')
        self.wireguard_interface = kwargs.get('interface_name')
        self.wireguard_address = kwargs.get('private_ip') + '/' + str(kwargs.get('private_subnet_mask'))
        self.wireguard_persistent_keepalive = kwargs.get('keep_alive')
        self.server_public_ip = self.host
        self.domain = settings.DOMAIN

    def run(self):
        """
        returns dict contains:
        {
            "wireguard_privatekey": "value"
            "wireguard_publickey": "value"
        }
        """

        self.extra_vars = {
            'ansible_ssh_pass': self.password,
            'ansible_sudo_pass': self.password,
            'server_public_ip': self.server_public_ip,
            'wireguard_port': self.wireguard_port,
            'wireguard_interface': self.wireguard_interface,
            'wireguard_address': self.wireguard_address,
            'wireguard_persistent_keepalive': self.wireguard_persistent_keepalive,
            'domain': self.domain
        }
        logger.info(f'running wireguard setup with: {self.extra_vars}')
        res = super().run()
        return res.get('msg', {
            "wireguard_privatekey": "val 1",
            "wireguard_publickey": "val 2"
        })
