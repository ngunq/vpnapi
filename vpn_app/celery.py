import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vpn_app.settings')

app = Celery('vpn_app', broker='amqp://guest:guest@localhost:5672')


# Set RabbitMQ as the result backend
app.conf.result_backend = 'rpc://'

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Set the concurrency level for Celery workers
app.conf.worker_concurrency = 4  # Adjust this number as needed

