# Generated by Django 4.2 on 2023-05-31 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_privateservervm_vm_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privateservervm',
            name='password',
            field=models.CharField(db_column='Password', max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='privateservervm',
            name='username',
            field=models.CharField(db_column='Username', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='privateservervm',
            name='vm_socket',
            field=models.IntegerField(db_column='VmSocket', null=True),
        ),
    ]
