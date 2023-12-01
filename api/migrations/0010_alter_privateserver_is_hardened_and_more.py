# Generated by Django 4.2 on 2023-06-03 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_privateservervm_vm_template_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privateserver',
            name='is_hardened',
            field=models.BooleanField(db_column='IsHardened', null=True),
        ),
        migrations.AlterField(
            model_name='privateservervm',
            name='username',
            field=models.CharField(db_column='Username', default='root', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='privateservervm',
            name='vm_cores',
            field=models.IntegerField(db_column='VmCores', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='privateservervm',
            name='vm_memory',
            field=models.IntegerField(db_column='VmMemory', max_length=100, null=True),
        ),
    ]