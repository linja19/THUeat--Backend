# Generated by Django 3.2.8 on 2021-11-26 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0039_stall_stalloperationtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='canteen',
            name='canteenFloor',
            field=models.CharField(default=None, max_length=10),
        ),
    ]
