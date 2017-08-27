from django.db import models
from django.db.models import CharField, DateTimeField, TextField


class LexemesField(models.TextField):

    description = "Lexemes resulting from PostGres text search pre-processing on a body of text"

    def __init__(self, *args, **kwargs):
        super(LexemesField, self).__init__(*args, **kwargs)

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
    lexemes = LexemesField()

    # TODO: method to transform source and external_identifier to an URL

