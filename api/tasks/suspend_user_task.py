from celery import shared_task
from django.db import transaction
from api.ansible_helpers import OpenvpnKillSession
from api.models import AppUser
import logging

from api.tasks.utils import send_notification

logger = logging.getLogger('ansible')


@shared_task(bind=True, name='suspend_user_task')
@transaction.atomic()
def suspend_user(self, user_id):
    send_notification(f'suspend user task in progress for task {self.request.id}')
    self.update_state(state='IN_PROGRESS')

    user = AppUser.objects.get(id=user_id)
    for session in user.publicserveropenvpnsession_set.all():
        kill_session = OpenvpnKillSession(
            host=session.server.ip,
            username=session.server.username,
            password=session.server.password,
            openvpn_username=session.user.username
        )
        try:
            res = kill_session.run()
        except Exception as e:
            logger.error(f'error killing session {e}')
        session.delete()

    for session in user.privateservervmopenvpnsession_set.all():
        kill_session = OpenvpnKillSession(
            host=session.server.ip,
            username=session.server.username,
            password=session.server.password,
            openvpn_username=session.user.username
        )
        try:
            res = kill_session.run()
        except Exception as e:
            logger.error(f'error killing session {e}')
        session.delete()

    for session in user.publicservervpnwireguardclient_set.all():
        session.delete()

    for session in user.privateservervpnwireguardclient_set.all():
        session.delete()
    send_notification(f'suspend user task done for task {self.request.id}')
    self.update_state(state='SUCCESS', meta={'message': 'Suspend user completed successfully'})
