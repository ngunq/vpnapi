from django.conf import settings
from django.core.management import BaseCommand, call_command
from django.db import DatabaseError

from api.models import AppUser


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            call_command('migrate')
            if not AppUser.objects.count() and settings.DEBUG:
                call_command('seed')
                print('data seed sucess')
        except DatabaseError as dbe:
            print('error in migration {}'.format(dbe))
        
        try:
            call_command('collectstatic', '--clear', '--noinput')
        
        except FileNotFoundError as fnf:
            print('error collecting static files {}'.format(fnf))

