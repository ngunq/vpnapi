import json
import logging
import os.path

from django.conf import settings

from .runner import AnsibleRunner
from .utils import get_mask

logger = logging.getLogger('ansible')


class OpenVpnSetup(AnsibleRunner):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__name__ = 'openvpn_setup'
        self.playbook_path = str(os.path.join(str(settings.BASE_DIR), 'api', 'ansible_helpers', 'Ansible', 'openvpn',
                                              'openvpnSetup.yaml'))

        self.openvpn_tcp_port = kwargs.get('tcp_port')
        self.openvpn_udp_port = kwargs.get('udp_port')
        self.openvpn_custom_dns = kwargs.get('dns').split(',')
        self.openvpn_server_tcp_network = kwargs.get('tcp_private_subnet')
        self.openvpn_server_udp_network = kwargs.get('udp_private_subnet')
        self.openvpn_server_tcp_netmask = get_mask(
                kwargs.get('tcp_private_subnet') + '/' + str(kwargs.get('tcp_private_subnet_mask')))
        self.openvpn_server_udp_netmask = get_mask(
                kwargs.get('udp_private_subnet') + '/' + str(kwargs.get('udp_private_subnet_mask')))
        self.server_public_ip = self.host
        self.domain = settings.DOMAIN
        self.openvpn_conf_json_content = ''
        self.hostname = kwargs.get('hostname')

        try:
            with open('openvpn_conf.json') as f:
                self.openvpn_conf_json_content = json.loads(f.read())
        except Exception as e:
            print(f'openvpn_conf not found {e}')

    def run(self, return_finalizer_data=True):

        self.extra_vars = {
            'ansible_ssh_pass': self.password,
            'ansible_sudo_pass': self.password,
            'server_public_ip': self.server_public_ip,
            'openvpn_tcp_port': self.openvpn_tcp_port,
            'openvpn_udp_port': self.openvpn_udp_port,
            'openvpn_custom_dns': self.openvpn_custom_dns,
            'openvpn_server_tcp_network': self.openvpn_server_tcp_network,
            'openvpn_server_udp_network': self.openvpn_server_udp_network,
            'openvpn_server_tcp_netmask': self.openvpn_server_tcp_netmask,
            'openvpn_server_udp_netmask': self.openvpn_server_udp_netmask,
            'openvpn_conf_json_content': self.openvpn_conf_json_content,
            'domain': self.domain
        }
        logger.info(f'running openvpn setup with: {self.extra_vars}')

        res = super().run()
        res = res.get('msg', {
            "openvpn_tcp_host": "uuid . domain :openvpn_tcp_port ",
            "openvpn_udp_host": "uuid . domain :openvpn_udp_port ",
            "openvpn_tcp_config": "tex \n\n t1tex  ttest",
            "openvpn_udp_config": "text2  test \n\n 123",
            "clients": ['client1']
        }) 
        # base_dir = os.path.dirname(self.playbook_path)
        # res['tcp_conf'] = os.path.join(base_dir, 'clients', self.host, self.hostname + '-tcp.ovpn')
        # res['udp_conf'] = os.path.join(base_dir, 'clients', self.host, self.hostname + '-udp.ovpn')
        logger.info(res)

        return res
