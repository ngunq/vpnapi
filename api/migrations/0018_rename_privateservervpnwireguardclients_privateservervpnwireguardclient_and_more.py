# Generated by Django 4.2 on 2023-06-11 13:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_rename_sessions_limit_appuser_openvpn_sessions_limit_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PrivateServerVpnWireguardClients',
            new_name='PrivateServerVpnWireguardClient',
        ),
        migrations.AlterField(
            model_name='publicserver',
            name='hostname',
            field=models.CharField(blank=True, db_column='HostName', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='publicserver',
            name='users',
            field=models.ManyToManyField(blank=True, db_table='PublicServerUsers', to=settings.AUTH_USER_MODEL),
        ),
    ]
