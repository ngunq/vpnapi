import ipaddress
import random

import faker
from django.core.management import BaseCommand
from django.db import transaction
from model_bakery import baker

from api.models import (AppUser, PrivateServerVPN, PrivateServer, PrivateServerVM,
                        Provider, PublicServer, PublicServerVPN, MgmtWhitelistedIp)


class Command(BaseCommand):
    
    fake = faker.Faker()
    
    def get_subnet(self):
        subnet = ipaddress.IPv4Network(random.randint(0,2000000000))
        return str(subnet)
    
    def get_name(self):
        return self.fake.text(max_nb_chars=20)
    
    def get_int(self):
        return random.randint(0,5000)
    
    def get_key(self):
        return self.fake.password(length=30)
    
    @transaction.atomic
    def handle(self, *args, **options):

        providers = baker.make(Provider, _quantity=30, name = self.get_name)
        
        mgmt_whitelisted_ips = baker.make(MgmtWhitelistedIp, _quantity=30, name = self.get_name)
        
        private_servers = baker.make(PrivateServer, _quantity=30, _fill_optional=True, 
                                    provider = lambda: providers[random.randint(0,len(providers)-1)],
                                    city = self.fake.city, country=self.fake.country, hostname=self.fake.domain_name,
                                    username=self.fake.user_name, name = self.get_name, password=self.fake.password,
                                    is_hardened=self.fake.pybool)
        
        
        private_server_vms = baker.make(PrivateServerVM, _quantity=30, _fill_optional=True, 
                                    private_server = lambda: private_servers[random.randint(0,len(private_servers)-1)],
                                    hostname=self.fake.domain_name, username=self.fake.user_name, name = self.get_name,
                                    password=self.fake.password, is_hardened=self.fake.pybool)
        
        
        private_server_vpns = baker.make(PrivateServerVPN, _quantity=30, _fill_optional=True, 
                                        port = self.get_int,
                                        private_server_vm = lambda: private_server_vms[random.randint(0,len(private_server_vms)-1)],
                                        private_subnet = self.get_subnet, config = self.fake.text, private_key=self.get_key,
                                        public_key=self.get_key, interface_name=self.get_name, keep_alive=self.get_int,
                                        dns = self.fake.ipv4)
        

        public_servers = baker.make(PublicServer, _quantity=30, _fill_optional=True, 
                                    provider = lambda: providers[random.randint(0,len(providers)-1)],
                                    city = self.fake.city, country=self.fake.country, hostname=self.fake.domain_name,
                                    username=self.fake.user_name, name = self.get_name, password=self.fake.password,
                                    is_hardened=self.fake.pybool)
        
        public_server_vpns = baker.make(PublicServerVPN, _quantity=30, _fill_optional=True, 
                                        port = self.get_int,
                                        public_server = lambda: public_servers[random.randint(0,len(public_servers)-1)],
                                        private_subnet = self.get_subnet, config = self.fake.text, private_key=self.get_key,
                                        public_key=self.get_key, interface_name=self.get_name, keep_alive=self.get_int,
                                        dns = self.fake.ipv4)
        

        admin = AppUser.objects.create_user(username='admin', password='123.com.net', is_staff=True, is_superuser=True, email='admin@mail.com')
        admin.save()

        test = AppUser.objects.create_user(username='test', password='test', is_staff=True, is_superuser=True, email='test@mail.com')
        test.save()

        user1 = AppUser.objects.create_user(username='user1', password='123.com.net', email='user1@mail.com', first_name='f', last_name='l')
        user1.save()
