# Generated by Django 4.2 on 2023-05-27 19:06

import uuid

import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

import api.helpers.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.PositiveSmallIntegerField(choices=[(1, 'Private'), (2, 'Public'), (3, 'Private Server Vm User')], db_column='UserType', default=1)),
                ('first_name', models.CharField(db_column='FirstName', max_length=150, verbose_name='First Name')),
                ('last_name', models.CharField(db_column='LastName', max_length=150, verbose_name='Last Name')),
                ('id', models.UUIDField(db_column='Id', default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'db_table': 'AppUsers',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='MgmtWhitelistedIp',
            fields=[
                ('id', models.UUIDField(db_column='Id', default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='Name', max_length=50)),
                ('ip', models.GenericIPAddressField(db_column='IP', protocol='IPv4')),
            ],
            options={
                'db_table': 'MgmtWhitelistedIp',
            },
        ),
        migrations.CreateModel(
            name='PrivateServer',
            fields=[
                ('id', models.UUIDField(db_column='Id', default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ip', models.GenericIPAddressField(db_column='IP', protocol='IPv4')),
                ('username', models.CharField(db_column='username', max_length=100, null=True)),
                ('password', models.CharField(db_column='Password', max_length=128)),
                ('city', models.CharField(db_column='City', max_length=100)),
                ('country', models.CharField(db_column='Country', max_length=100)),
                ('is_hardened', models.BooleanField(db_column='IsHardened', default=False)),
                ('hostname', models.CharField(db_column='HostName', max_length=100, null=True)),
                ('name', models.CharField(db_column='Name', max_length=100, null=True)),
                ('status', models.BooleanField(db_column='Status', null=True)),
            ],
            options={
                'db_table': 'PrivateServers',
            },
        ),
        migrations.CreateModel(
            name='PrivateServerVM',
            fields=[
                ('id', models.UUIDField(db_column='Id', default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='Name', max_length=50)),
                ('ip', models.GenericIPAddressField(db_column='IP', null=True, protocol='IPv4')),
                ('username', models.CharField(db_column='Username', max_length=50)),
                ('password', models.CharField(db_column='Password', max_length=128)),
                ('is_hardened', models.BooleanField(db_column='IsHardened', default=False)),
                ('hostname', models.CharField(db_column='HostName', max_length=100, null=True)),
                ('status', models.BooleanField(db_column='Status', null=True)),
                ('private_server', models.ForeignKey(db_column='PrivateServerId', on_delete=django.db.models.deletion.CASCADE, to='api.privateserver')),
            ],
            options={
                'db_table': 'PrivateServersVM',
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.UUIDField(db_column='Id', default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='Name', max_length=100)),
            ],
            options={
                'db_table': 'Providers',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='PublicServer',
            fields=[
                ('id', models.UUIDField(db_column='Id', default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ip', models.GenericIPAddressField(blank=True, db_column='IP', null=True, protocol='IPv4')),
                ('username', models.CharField(db_column='username', max_length=100, null=True)),
                ('password', models.CharField(db_column='Password', max_length=128)),
                ('city', models.CharField(db_column='City', max_length=100)),
                ('country', models.CharField(db_column='Country', max_length=100)),
                ('is_hardened', models.BooleanField(db_column='IsHardened', default=False)),
                ('hostname', models.CharField(db_column='HostName', max_length=100, null=True)),
                ('name', models.CharField(db_column='Name', max_length=100, null=True)),
                ('status', models.BooleanField(db_column='Status', null=True)),
                ('provider', models.ForeignKey(db_column='ProviderId', on_delete=django.db.models.deletion.CASCADE, to='api.provider')),
                ('users', models.ManyToManyField(db_table='PublicServerUsers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'PublicServers',
            },
        ),
        migrations.CreateModel(
            name='PublicServerVPN',
            fields=[
                ('id', models.UUIDField(db_column='Id', default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('port', models.IntegerField(db_column='Port', null=True)),
                ('status', models.BooleanField(db_column='Status', null=True)),
                ('config', models.TextField(db_column='Config', null=True)),
                ('vpn_type', models.PositiveSmallIntegerField(choices=[(1, 'Openvpn'), (2, 'Wireguard')], db_column='VpnType', null=True)),
                ('transport', models.PositiveSmallIntegerField(choices=[(1, 'Tcp'), (2, 'Udp')], db_column='Transport', null=True)),
                ('private_subnet', models.CharField(db_column='PrivateSubnet', max_length=50, null=True)),
                ('private_subnet_mask', models.CharField(db_column='PrivateSubnetMask', max_length=50, null=True)),
                ('private_ip', models.GenericIPAddressField(db_column='PrivateIP', null=True, protocol='IPv4')),
                ('private_key', models.CharField(db_column='PrivateKey', max_length=100, null=True)),
                ('public_key', models.CharField(db_column='PublicKey', max_length=100, null=True)),
                ('interface_name', models.CharField(db_column='InterfaceName', max_length=100, null=True)),
                ('dns', models.CharField(db_column='dns', max_length=100, null=True)),
                ('keep_alive', models.IntegerField(db_column='KeepAlive', null=True)),
                ('public_server', models.ForeignKey(db_column='ServerId', on_delete=django.db.models.deletion.CASCADE, to='api.publicserver')),
            ],
            options={
                'db_table': 'PublicServersVPNs',
            },
        ),
        migrations.CreateModel(
            name='PrivateServerVPN',
            fields=[
                ('id', models.UUIDField(db_column='Id', default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('port', models.IntegerField(db_column='Port', null=True)),
                ('status', models.BooleanField(db_column='Status', null=True)),
                ('config', models.TextField(db_column='Config', null=True)),
                ('vpn_type', models.PositiveSmallIntegerField(choices=[(1, 'Openvpn'), (2, 'Wireguard')], db_column='VpnType', null=True)),
                ('transport', models.PositiveSmallIntegerField(choices=[(1, 'Tcp'), (2, 'Udp')], db_column='Transport', null=True)),
                ('private_subnet', models.CharField(db_column='PrivateSubnet', max_length=50, null=True, validators=[api.helpers.validators.validate_subnet])),
                ('private_subnet_mask', models.CharField(db_column='PrivateSubnetMask', max_length=50, null=True)),
                ('private_ip', models.GenericIPAddressField(db_column='PrivateIP', null=True, protocol='IPv4')),
                ('private_key', models.CharField(db_column='PrivateKey', max_length=100, null=True)),
                ('public_key', models.CharField(db_column='PublicKey', max_length=100, null=True)),
                ('interface_name', models.CharField(db_column='InterfaceName', max_length=100, null=True)),
                ('dns', models.CharField(db_column='dns', max_length=100, null=True)),
                ('keep_alive', models.IntegerField(db_column='KeepAlive', null=True)),
                ('private_server_vm', models.ForeignKey(db_column='PrivateServerVMId', on_delete=django.db.models.deletion.CASCADE, to='api.privateservervm')),
            ],
            options={
                'db_table': 'PrivateServersVPNs',
            },
        ),
        migrations.CreateModel(
            name='PrivateServerUser',
            fields=[
                ('id', models.UUIDField(db_column='Id', default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('private_server', models.ForeignKey(db_column='PrivateServerId', on_delete=django.db.models.deletion.CASCADE, to='api.privateserver')),
                ('user', models.ForeignKey(db_column='UserId', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'PrivateServerUsers',
            },
        ),
        migrations.AddField(
            model_name='privateserver',
            name='provider',
            field=models.ForeignKey(db_column='ProviderId', on_delete=django.db.models.deletion.CASCADE, to='api.provider'),
        ),
        migrations.AddField(
            model_name='privateserver',
            name='users',
            field=models.ManyToManyField(through='api.PrivateServerUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appuser',
            name='private_server_vm',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.privateservervm'),
        ),
        migrations.AddField(
            model_name='appuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
