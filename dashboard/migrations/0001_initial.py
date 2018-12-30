# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-12-30 08:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('name', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('email', models.CharField(blank=True, max_length=500, null=True)),
                ('phone', models.CharField(blank=True, max_length=500, null=True)),
                ('pan', models.CharField(blank=True, max_length=500, null=True)),
                ('tan', models.CharField(blank=True, max_length=500, null=True)),
                ('gst', models.CharField(blank=True, max_length=500, null=True)),
                ('address', models.CharField(blank=True, max_length=3000, null=True)),
                ('type', models.CharField(blank=True, max_length=3000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('name', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('email', models.CharField(blank=True, max_length=500, null=True)),
                ('phone', models.CharField(blank=True, max_length=500, null=True)),
                ('pan', models.CharField(blank=True, max_length=500, null=True)),
                ('tan', models.CharField(blank=True, max_length=500, null=True)),
                ('gst', models.CharField(blank=True, max_length=500, null=True)),
                ('address', models.CharField(blank=True, max_length=3000, null=True)),
                ('type', models.CharField(blank=True, max_length=3000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Technologies',
            fields=[
                ('name', models.CharField(max_length=500, primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='supplier',
            name='technologies',
            field=models.ManyToManyField(to='dashboard.Technologies'),
        ),
    ]