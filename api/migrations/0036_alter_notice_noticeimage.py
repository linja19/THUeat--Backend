# Generated by Django 3.2.8 on 2021-11-25 22:56

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0035_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='noticeImage',
            field=models.ImageField(blank=True, default='default/default_notice.jpg', null=True, upload_to=api.models.get_file_path_notice),
        ),
    ]
