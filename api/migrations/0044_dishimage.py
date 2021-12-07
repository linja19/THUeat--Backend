# Generated by Django 3.2.8 on 2021-12-07 22:01

import api.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0043_alter_stall_stalloperationtime'),
    ]

    operations = [
        migrations.CreateModel(
            name='DishImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dishImage', models.ImageField(blank=True, default='default/default_dish.png', null=True, upload_to=api.models.get_file_path_dish)),
                ('dishID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.dish')),
            ],
        ),
    ]
