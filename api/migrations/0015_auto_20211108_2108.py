# Generated by Django 3.2.8 on 2021-11-08 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20211108_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='dishLikes',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='reviewLikes',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stall',
            name='stallRate',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stall',
            name='stallRateNum',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
