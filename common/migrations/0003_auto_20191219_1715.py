# Generated by Django 2.1.7 on 2019-12-19 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20191219_1447'),
    ]

    operations = [
        migrations.RenameField(
            model_name='policy',
            old_name='categoryName',
            new_name='Name',
        ),
        migrations.AlterField(
            model_name='policy',
            name='num',
            field=models.IntegerField(blank=True, max_length=1000, null=True),
        ),
    ]