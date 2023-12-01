import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class TaskNotificationConsumer(WebsocketConsumer):
    def connect(self):
        # print(self.scope['user'])
        group = 'admin'
        async_to_sync(self.channel_layer.group_add)(group, self.channel_name)
        self.accept()
        self.send(text_data=json.dumps({'hi': 'hi'}))

    def disconnect(self, code):
        group = 'admin'
        async_to_sync(self.channel_layer.group_discard)(group, self.channel_name)

    def task_notification(self, event):
        self.send(text_data=json.dumps(event['data']))
