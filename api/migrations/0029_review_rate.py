# Generated by Django 3.2.8 on 2021-11-24 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_auto_20211124_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='rate',
            field=models.FloatField(default=None),
        ),
    ]
