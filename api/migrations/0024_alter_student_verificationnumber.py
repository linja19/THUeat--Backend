# Generated by Django 3.2.8 on 2021-11-23 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_auto_20211124_0018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='verificationNumber',
            field=models.CharField(default=None, max_length=6),
        ),
    ]
