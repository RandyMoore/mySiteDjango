# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-28 00:24
from __future__ import unicode_literals

from django.db import migrations, models
import government_audit.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuditDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publication_date', models.DateTimeField()),
                ('title', models.CharField(max_length=100)),
                ('source', models.CharField(choices=[('AO', 'archive.org')], max_length=2)),
                ('external_identifier', models.CharField(max_length=100)),
                ('lexemes', government_audit.models.LexemesField(null=True)),
                ('text', models.TextField(default='')),
            ],
        ),
    ]
