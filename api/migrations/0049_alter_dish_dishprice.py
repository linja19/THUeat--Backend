# Generated by Django 3.2.8 on 2021-12-15 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0048_alter_stall_stallrate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='dishPrice',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]