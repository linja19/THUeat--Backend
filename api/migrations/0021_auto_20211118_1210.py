# Generated by Django 3.2.8 on 2021-11-18 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_auto_20211118_0042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='dishLikes',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='reviewLikes',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
