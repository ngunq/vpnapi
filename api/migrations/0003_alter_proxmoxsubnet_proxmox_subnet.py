# Generated by Django 4.2 on 2023-05-29 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_privateserver_proxmox_default_disk_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proxmoxsubnet',
            name='proxmox_subnet',
            field=models.CharField(db_column='ProxmoxSubnet', max_length=50, null=True),
        ),
    ]