# Generated by Django 3.2.8 on 2021-11-17 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_replybystaff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='replybystaff',
            name='replyDateTime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='reviewDateTime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]