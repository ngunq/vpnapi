import json
import logging
import os
from datetime import datetime
from pathlib import Path

from django.conf import settings

from api.utils.crypto import decrypt

logger = logging.getLogger('ansible')


class AnsibleRunner:

    def __init__(self, **kwargs):
        self.username = kwargs.get('username')
        self.host = kwargs.get('host')
        self.password = decrypt(kwargs.get('password'))
        self.playbook_path = None
        self.extra_vars = None
        self.__name__ = 'ansible'

    def run(self):
        inventory = {
            'all': {
                'hosts': {
                    self.host: {
                        'ansible_host': self.host,
                        'ansible_user': self.username,
                        'ansible_password': self.password,
                        'ansible_connection': 'ssh',
                        'ansible_ssh_common_args': '-o StrictHostKeyChecking=no'
                    }
                }
            }
        }

        try:
            import ansible_runner
            runner = ansible_runner.run(
                playbook=self.playbook_path,
                inventory=inventory,
                extravars=self.extra_vars,
                quiet=True,
                # json_mode=True,
                private_data_dir=os.path.join(
                    str(settings.BASE_DIR), Path('ansible_log/ansible_runner_data')),
                ident=self.__name__ + '-' + \
                datetime.now().strftime('%Y-%m-%d_%H-%M-%S.%f')[:-3],
                rotate_artifacts=100
            )
            errors = ''
            for event in runner.events:
                if event['event'] == 'runner_on_ok' and event['event_data']['task'] == 'Finalizer':
                    data = event['stdout'].split('=>')
                    data = json.loads(data[1])
                    logger.info(data)
                    return data
                if event['event'] == 'runner_on_unreachable':
                    raise ValueError(
                        'host unreachable check the ip,username and/or password')
                if event['event'] == 'runner_on_failed':
                    errors += event['stdout'] + '\n'

            logger.error(f'finalizer data not found {errors}')
            raise ValueError(f'finalizer data not found {errors}')

        except ImportError:
            logger.warning('ansible import error')
            return {}
