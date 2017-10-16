from django.db import models
from django.db.models import CharField, DateField, IntegerField, FloatField, ForeignKey, Func, TextField, Value


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
    url = CharField(max_length=256, blank=False)
    rank = FloatField(null=True)

    def save(self, *args, **kwargs):
        self.lexemes = Func(Value('english'), Value(self.title + ' ' + self.text), function='to_tsvector')
        self.text = '' # Not needed for search only
        super(AuditDocument, self).save(*args, **kwargs)


class NamedEntity(models.Model):
    document = ForeignKey(AuditDocument, on_delete=models.CASCADE)
    name = CharField(max_length=64, blank=False)
    frequency = IntegerField(blank=False)