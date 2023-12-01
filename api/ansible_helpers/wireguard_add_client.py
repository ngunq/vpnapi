import logging
import os.path

from django.conf import settings

from .runner import AnsibleRunner

logger = logging.getLogger('ansible')


class WireguardAddClient(AnsibleRunner):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__name__ = 'wireguard_add_client'
        self.playbook_path = str(os.path.join(str(settings.BASE_DIR), 'api', 'ansible_helpers', 'Ansible', 'wireguard',
                                              'wireguardAddClient.yaml'))

        self.clientusername = kwargs.get('client_username')
        self.wireguard_port = kwargs.get('port')
        self.wireguard_interface = kwargs.get('interface_name')
        self.wireguard_dns = kwargs.get('dns')
        self.wireguard_address = kwargs.get('private_ip') + '/' + str(kwargs.get('private_subnet_mask'))
        self.wireguard_persistent_keepalive = kwargs.get('keep_alive')
        self.hostname = kwargs.get('hostname')

    def run(self):
        """
        returns dict contains:
        {
            client_config_text: "{{ client_config_text.stdout }}"
            client_qr_code_base64: "{{ qr_code_base64.stdout }}"
        }
        """
        self.extra_vars = {
            'ansible_ssh_pass': self.password,
            'ansible_sudo_pass': self.password,
            'username': self.clientusername,
            'wireguard_address': self.wireguard_address,
            'wireguard_port': self.wireguard_port,
            'wireguard_interface': self.wireguard_interface,
            'wireguard_dns': self.wireguard_dns,
            'wireguard_persistent_keepalive': self.wireguard_persistent_keepalive,
            'hostname': self.hostname
        }
        logger.info(f'running wireguard add client with: {self.extra_vars}')
        res = super().run()

        # res = {}
        # base_dir = os.path.dirname(self.playbook_path)
        # config_path = os.path.join(base_dir, 'clients', self.host, self.clientusername,
        #                            self.hostname + '-full.conf')
        # qr_path = os.path.join(base_dir, 'clients', self.host, self.clientusername, self.hostname + '-qr-full')
        # res['config_path'] = config_path
        # res['qr_path'] = qr_path
        return res.get('msg', {
            "client_config_text": "test",
            "client_qr_code_base64": "tes54"
        })
