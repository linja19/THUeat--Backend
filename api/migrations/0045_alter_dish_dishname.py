# Generated by Django 3.2.8 on 2021-12-07 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0044_dishimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='dishName',
            field=models.CharField(max_length=30),
        ),
    ]