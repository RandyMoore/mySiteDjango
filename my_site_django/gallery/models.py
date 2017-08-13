from django.db import models
from django.db.models import CharField, DecimalField, ImageField, TextField, TimeField


class Image(models.Model):
    image_data = ImageField()
    title = CharField(max_length=100, null=True)
    description = TextField(null=True)
    time_taken = TimeField(auto_now_add=True)
    geo_lat = DecimalField(max_digits=12, decimal_places=9, null=True)
    geo_lon = DecimalField(max_digits=12, decimal_places=9, null=True)

    class Meta:
        ordering = ('time_taken',)