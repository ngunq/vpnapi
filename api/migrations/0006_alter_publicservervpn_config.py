# Generated by Django 4.2 on 2023-05-31 11:12

from django.db import migrations, models

import api.helpers.upload_helpers


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_privateservervm_password_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicservervpn',
            name='config',
            field=models.FileField(db_column='Config', null=True, upload_to=api.helpers.upload_helpers.upload_ovpn),
        ),
    ]
