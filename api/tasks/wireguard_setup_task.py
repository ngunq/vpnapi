import logging

from celery import shared_task
from celery.result import AsyncResult
from django.db import transaction

from api.ansible_helpers import WireguardSetup
from api.serializers import PrivateServerVpnWireguardWriteSerializer, PublicServerVpnWireguardWriteSerializer
from api.tasks.utils import send_notification

logger = logging.getLogger('ansible')


@shared_task(bind=True, name='private wireguard setup task')
@transaction.atomic()
def handle_private_vpn_wireguard_setup(self, data):
    self.update_state(state='IN_PROGRESS')
    send_notification(f'wireguard setup task in progress for task {self.request.id}')
    try:
        serializer = PrivateServerVpnWireguardWriteSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
    except Exception as e:
        logger.error(e)
        send_notification(f'wireguard setup task failed for task {self.request.id}')
        raise ValueError(f'error creating object {e}')

    try:
        wireguard_setup = WireguardSetup(
            **serializer.data,
            host=instance.private_server_vm.ip,
            username=instance.private_server_vm.username,
            password=instance.private_server_vm.password
        )
        res = wireguard_setup.run()
        instance.private_key = res.get('wireguard_privatekey')
        instance.public_key = res.get('wireguard_publickey')
        instance.save()
        logger.info(f'Wireguard Setup completed successfully')
        send_notification(f'wireguard setup task done for task {self.request.id}')
        return {'id': instance.id}
    except Exception as e:
        logger.info(f'Wireguard Setup Failed')
        logger.error(e)
        instance.delete()
        send_notification(f'wireguard setup task failed for task {self.request.id}')
        raise ValueError(f'Wireguard setup failed {e}')
        # self.update_state(state='FAILURE', meta={'message': 'Wireguard setup failed', 'error_message': str(e)})


@shared_task(bind=True, name='public vpn wireguard setup task')
@transaction.atomic()
def handle_public_vpn_wireguard_setup(self, data):
    send_notification(f'wireguard setup task in progress for task {self.request.id}')
    try:
        self.update_state(state='IN_PROGRESS')
        serializer = PublicServerVpnWireguardWriteSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
    except Exception as e:
        logger.error(e)
        send_notification(f'wireguard setup task failed for task {self.request.id}')
        raise ValueError(f'error creating object {e}')

    try:
        wireguard_setup = WireguardSetup(
            **serializer.data, host=instance.public_server.ip,
            username=instance.public_server.username,
            password=instance.public_server.password
        )
        res = wireguard_setup.run()
        instance.private_key = res.get('wireguard_privatekey')
        instance.public_key = res.get('wireguard_publickey')
        instance.save()
        logger.info(f'Wireguard Setup completed successfully')
        send_notification(f'wireguard setup task done for task {self.request.id}')
        return {'id': instance.id}
    except Exception as e:
        logger.info(f'Wireguard Setup Failed')
        instance.delete()
        logger.error(e)
        send_notification(f'wireguard setup failed for task {self.request.id}')
        raise ValueError(f'Wireguard setup failed {e}')
        # self.update_state(state='FAILURE', meta={'message': 'Wireguard setup failed', 'error_message': str(e)})
