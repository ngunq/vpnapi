from .consumers import TaskNotificationConsumer
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'ws/notifications', TaskNotificationConsumer.as_asgi())
]