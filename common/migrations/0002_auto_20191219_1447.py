# Generated by Django 2.1.7 on 2019-12-19 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='policy',
            name='num',
            field=models.IntegerField(blank=True, max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='policy',
            name='updateTime',
            field=models.DateTimeField(blank=True, max_length=10000, null=True),
        ),
        migrations.AlterField(
            model_name='policy',
            name='url',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
