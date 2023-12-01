from api.views import get_task_status
from api.views import get_tasks_list

from django.urls import path


celery_urlpatterns = [
    path('Celery/GetTaskStatus', get_task_status),
    path('Celery/GetTasksList', get_tasks_list)
]
