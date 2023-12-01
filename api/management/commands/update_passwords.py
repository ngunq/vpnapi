from django.core.management import BaseCommand
from django.db import transaction
from api.models import PrivateServer, PrivateServerVM, PublicServer
from api.utils.crypto import encrypt


class Command(BaseCommand):

    @transaction.atomic()
    def handle(self, *args, **options):
        for server in PrivateServer.objects.all():
            server.password = encrypt(server.password)
            server.save()
        
        for server in PublicServer.objects.all():
            server.password = encrypt(server.password)
            server.save()
        
        for server in PrivateServerVM.objects.all():
            server.password = encrypt(server.password)
            server.save()

