from rest_framework.serializers import ModelSerializer

from .models import AuditDocument


class AuditDocumentSerializer(ModelSerializer):

    class Meta:
        model = AuditDocument
        fields = ('id', 'publication_date', 'title', 'source', 'external_identifier', 'text')
