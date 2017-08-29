from django.db import models
from django.db.models import CharField, DateTimeField, F, Func, TextField, Value


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

    publication_date = DateTimeField(auto_now_add=False)
    title = CharField(max_length=1024, blank=False)
    source = CharField(max_length=2, blank=False, choices=SOURCES)
    external_identifier = CharField(max_length=100, blank=False)
    lexemes = LexemesField(null=True)
    text = TextField(default='')

    def save(self, *args, **kwargs):
        self.lexemes = Func(Value('english'), Value(self.text), function='to_tsvector')
        super(AuditDocument, self).save(*args, **kwargs)