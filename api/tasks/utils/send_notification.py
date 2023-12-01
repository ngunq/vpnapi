from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_notification(data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)('admin', {
        'data': data,
        'type': 'task.notification'
    })
