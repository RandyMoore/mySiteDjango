from django.db import models
from django.db.models import (NullBooleanField, CharField, DateField, IntegerField, FloatField, ForeignKey, Func,
                              TextField, Value)
from django.contrib.postgres.indexes import GinIndex

class LexemesField(models.Field):
    description = "Lexemes resulting from PostGres text search pre-processing on a body of text"

    def __init__(self, *args, **kwargs):
        super(LexemesField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'tsvector'


class AuditDocument(models.Model):
    SOURCES = (
        ('AO', 'archive.org'),
    )

    publication_date = DateField(auto_now_add=False)
    title = CharField(max_length=1024, blank=False)
    source = CharField(max_length=2, blank=False, choices=SOURCES)
    lexemes = LexemesField(null=True)
    text = TextField(default='')
    url = CharField(max_length=1024, blank=True, null=True)
    rank = FloatField(null=True)
    path = CharField(max_length=256, blank=False, default='')
    url_active = NullBooleanField()

    def save(self, *args, **kwargs):
        self.lexemes = Func(Value('english'), Value(self.title + ' ' + self.text), function='to_tsvector')
        self.text = '' # Not needed for search only
        super(AuditDocument, self).save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['publication_date']),
            GinIndex(fields=['lexemes']),
        ]


class NamedEntity(models.Model):
    document = ForeignKey(AuditDocument, on_delete=models.CASCADE, related_name='named_entities')
    name = CharField(max_length=64, blank=False)
    frequency = IntegerField(blank=False)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['document']),
        ]