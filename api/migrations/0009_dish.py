# Generated by Django 3.2.8 on 2021-11-07 17:45

import api.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_stall'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('dishID', models.BigAutoField(primary_key=True, serialize=False)),
                ('dishName', models.CharField(max_length=30, unique=True)),
                ('dishPrice', models.FloatField()),
                ('dishImage', models.ImageField(blank=True, default='default_canteen.jpg', null=True, upload_to=api.models.get_file_path_canteen)),
                ('dishDescribe', models.CharField(blank=True, max_length=300)),
                ('dishLikes', models.IntegerField(blank=True)),
                ('dishAvailableTime', models.CharField(default='1234', max_length=4)),
                ('stallID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.stall')),
            ],
        ),
    ]
