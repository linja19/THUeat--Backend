# Generated by Django 3.2.8 on 2021-11-24 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_alter_stall_stallratenum'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Ratings',
        ),
    ]