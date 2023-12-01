import logging

from celery import shared_task
from channels.layers import get_channel_layer
from django.db import transaction
from api.tasks.utils.send_notification import send_notification
from api.ansible_helpers import OpenvpnKillSession
from api.models import PublicServerOpenvpnSession

logger = logging.getLogger('ansible')


@shared_task(bind=True, name='kill_session_task')
@transaction.atomic()
def handle_kill_session(self, session_id):
    
    try:
        self.update_state(state='IN_PROGRESS')

        send_notification(f'starting killsession on {session_id}')
        session = PublicServerOpenvpnSession.objects.get(id=session_id)
        kill_session = OpenvpnKillSession(
            host=session.server.ip,
            username=session.server.username,
            password=session.server.password,
            openvpn_username=session.user.username
        )
        res = kill_session.run()
        if not res:
            logger.error(f'killing session {session_id} failed')
            return
        session.delete()
        logger.info(f'killing session {session_id} succeeded')
        send_notification(f'killing session {session_id} succeeded')
        self.update_state(state='SUCCESS', meta={'message': 'Killing Session completed successfully'})
    except Exception as e:
        logger.error(f'killing failed {e}')
        # self.update_state(state='FAILURE', meta={'message': 'Killing Session failed', 'error_message': str(e)})
        send_notification(f'killing session failed on task {self.request.id}')
        raise ValueError(f'killing session failed {e}')
