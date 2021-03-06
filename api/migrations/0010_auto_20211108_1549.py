# Generated by Django 3.2.8 on 2021-11-08 07:49

import api.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_dish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='canteen',
            name='canteenImage',
            field=models.ImageField(blank=True, default='default/default_canteen.jpg', null=True, upload_to=api.models.get_file_path_canteen),
        ),
        migrations.AlterField(
            model_name='dish',
            name='dishImage',
            field=models.ImageField(blank=True, default='default/default_dish.jpg', null=True, upload_to=api.models.get_file_path_dish),
        ),
        migrations.AlterField(
            model_name='stall',
            name='stallImage',
            field=models.ImageField(blank=True, default='default/default_stall.jpg', null=True, upload_to=api.models.get_file_path_stall),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('reviewID', models.BigAutoField(primary_key=True, serialize=False)),
                ('reviewDateTime', models.DateTimeField(auto_now=True)),
                ('reviewLikes', models.IntegerField(blank=True)),
                ('reviewComment', models.CharField(blank=True, max_length=500)),
                ('reviewImages', models.ImageField(blank=True, null=True, upload_to=api.models.get_file_path_review)),
                ('reviewTags', models.CharField(blank=True, max_length=100)),
                ('reply', models.BooleanField(default=False)),
                ('stallID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.stall')),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
