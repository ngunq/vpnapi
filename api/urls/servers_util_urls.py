from api.views import decrypt_password

from django.urls import path

server_util_urls = [
    path('Server/DecryptPassword', decrypt_password)
]