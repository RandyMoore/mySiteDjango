# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-16 20:40
from __future__ import unicode_literals

import django.contrib.postgres.indexes
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('government_audit', '0003_namedentity'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='auditdocument',
            index=models.Index(fields=['publication_date'], name='government__publica_166516_idx'),
        ),
        migrations.AddIndex(
            model_name='auditdocument',
            index=django.contrib.postgres.indexes.GinIndex(fields=['lexemes'], name='government__lexemes_ad603a_gin'),
        ),
        migrations.AddIndex(
            model_name='namedentity',
            index=models.Index(fields=['name'], name='government__name_10a653_idx'),
        ),
        migrations.AddIndex(
            model_name='namedentity',
            index=models.Index(fields=['document'], name='government__documen_a49fa5_idx'),
        ),
    ]