from django.db import models
from django.db.models import CharField, DateTimeField, TextField


class LexemesField(models.Field):
    def db_type(self, connection):
        return 'tsvector'


class AuditDocument(models.Model):
    SOURCES = (
        ('AO', 'archive.org'),
    )

    publication_date = DateTimeField(auto_now_add=False)
    title = CharField(max_length=100, blank=False)
    source = CharField(max_length=2, blank=False, choices=SOURCES)
    external_identifier = CharField(max_length=100, blank=False)
    lexemes = LexemesField(null=True)
    text = TextField(default='')