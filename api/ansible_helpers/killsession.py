import os

from django.conf import settings

from .runner import AnsibleRunner


class OpenvpnKillSession(AnsibleRunner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__name__ = 'openvpn_killsession'
        self.playbook_path = str(os.path.join(str(settings.BASE_DIR), 'api', 'ansible_helpers', 'Ansible', 'openvpn',
                                              'openvpnKillSession.yaml'))
        self.openvpn_user = kwargs.get('openvpn_username')
        self.__name__ = 'openvpn_kill_session'

    def run(self):
        self.extra_vars = {
            'ansible_ssh_pass': self.password,
            'ansible_sudo_pass': self.password,
            'openvpn_user': self.openvpn_user
        }
        res = super().run()
        for i in res['msg']['details']:
            i = i.lower()
            if i.startswith('success'):
                return True

        return False
