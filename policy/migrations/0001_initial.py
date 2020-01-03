# Generated by Django 3.0.1 on 2020-01-03 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='talentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeName', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='strategy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.SlugField(blank=True, max_length=100, null=True)),
                ('level', models.CharField(blank=True, max_length=100, null=True)),
                ('updatetime', models.CharField(blank=True, max_length=100, null=True)),
                ('addr', models.CharField(blank=True, max_length=100, null=True)),
                ('content', models.CharField(blank=True, max_length=1000, null=True)),
                ('province', models.CharField(blank=True, max_length=50, null=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('intent', models.CharField(blank=True, max_length=100, null=True)),
                ('talent', models.ManyToManyField(to='policy.talentType')),
            ],
        ),
        migrations.CreateModel(
            name='MethodAndType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(blank=True, max_length=200, null=True)),
                ('type', models.CharField(blank=True, max_length=100, null=True)),
                ('province', models.CharField(blank=True, max_length=100, null=True)),
                ('stag', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='policy.strategy')),
            ],
        ),
    ]
