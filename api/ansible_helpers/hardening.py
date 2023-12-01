import logging

from django.conf import settings

from api.models import MgmtWhitelistedIp
from .runner import AnsibleRunner

logger = logging.getLogger('ansible')


class Hardening(AnsibleRunner):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__name__ = 'hardening'
        self.playbook_path = str(
            settings.BASE_DIR) + '/api/ansible_helpers/Ansible/hardening/hardening.yaml'
        self.allowed_ssh_ips_list = [
            ip for ip in MgmtWhitelistedIp.objects.values_list('ip', flat=True)]
        self.domain = settings.DOMAIN
        self.cloudflare_api_token = settings.CLOUDFLARE_API_TOKEN
        self.cloudflare_email = settings.CLOUDFLARE_EMAIL

    def run(self):
        """
        returns the uuid from finalizer after hardening is done
        """

        self.extra_vars = {
            'ansible_ssh_pass': self.password,
            'ansible_sudo_pass': self.password,
            'allowed_ssh_ips': self.allowed_ssh_ips_list,
            'domain': self.domain,
            'cloudflare_api_token': self.cloudflare_api_token,
            'cloudflare_email': self.cloudflare_email
        }
        logger.info(f'running hardening with: {self.extra_vars}')
        data = super().run()
        return data["msg"]["uuid"]
