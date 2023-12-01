import logging

from celery import shared_task
from celery.result import AsyncResult
from django.core.files import File
from django.db import transaction

from api.ansible_helpers import OpenVpnSetup
from api.serializers import PrivateServerVpnOpenvpnWriteSerializer, PublicServerVpnOpenvpnWriteSerializer
from api.tasks.utils import send_notification

logger = logging.getLogger('ansible')


@shared_task(bind=True, name='private_vm openvpn setup task')
@transaction.atomic()
def handle_privatevm_openvpn_setup(self, data):
    send_notification(f'openvpn setup task in progress for task {self.request.id}')
    self.update_state(state='IN_PROGRESS')
    serializer = PrivateServerVpnOpenvpnWriteSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    tcp_instance, udp_instance, openvpn_data = serializer.save()

    try:
        openvpn_setup = OpenVpnSetup(
            **openvpn_data,
            host=tcp_instance.private_server_vm.ip,
            username=tcp_instance.private_server_vm.username,
            password=tcp_instance.private_server_vm.password,
            hostname=tcp_instance.private_server_vm.hostname
        )
        res = openvpn_setup.run()

        tcp_instance.config = res.get('openvpn_tcp_config')
        tcp_instance.save()

        udp_instance.config = res.get('openvpn_udp_config')
        udp_instance.save()

        logger.info(f'OpenVPN Setup completed successfully')
        send_notification(f'openvpn setup task done for task {self.request.id}')
        self.update_state(state='SUCCESS', meta={'message': 'OpenVPN Setup completed successfully'})
        return {'tcp_id': str(tcp_instance.id), 'udp_id': str(udp_instance.id)}
    except Exception as e:
        logger.error(f'Openvpn Setup Failed')
        logger.error(e)
        send_notification(f'openvpn setup task failed for task {self.request.id}')
        raise ValueError(f'Openvpn setup failed: {e}')


@shared_task(bind=True, name='public openvpn setup task')
@transaction.atomic()
def handle_public_openvpn_setup(self, data):
    self.update_state(state='IN_PROGRESS')
    send_notification(f'openvpn setup task in progress for task {self.request.id}')
    serializer = PublicServerVpnOpenvpnWriteSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    tcp_instance, udp_instance, openvpn_data = serializer.save()
    try:
        openvpn_setup = OpenVpnSetup(
            **openvpn_data,
            host=tcp_instance.public_server.ip,
            username=tcp_instance.public_server.username,
            password=tcp_instance.public_server.password,
            hostname=tcp_instance.public_server.hostname,
        )
        res = openvpn_setup.run()

        tcp_instance.config = res.get('openvpn_tcp_config')
        tcp_instance.save()

        udp_instance.config = res.get('openvpn_udp_config')
        udp_instance.save()
        logger.info(f'OpenVPN Setup completed successfully')
        self.update_state(state='SUCCESS', meta={'message': 'OpenVPN Setup completed successfully'})
        send_notification(f'openvpn setup task done for task {self.request.id}')
        return {'tcp_id': str(tcp_instance.id), 'udp_id': str(udp_instance.id)}
    except Exception as e:
        logger.error(f'Openvpn Setup Failed')
        logger.error(e)
        send_notification(f'openvpn setup task failed for task {self.request.id}')
        raise ValueError(f'Openvpn setup failed {e}')
