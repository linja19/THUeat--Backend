# Generated by Django 3.2.8 on 2021-11-26 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0038_canteen_canteenphone'),
    ]

    operations = [
        migrations.AddField(
            model_name='stall',
            name='stallOperationtime',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
