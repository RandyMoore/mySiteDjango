from rest_framework import serializers
from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'title', 'image_data', 'description', 'time_taken', 'geo_lat', 'geo_lon',)
