from rest_framework import generics

from .models import AuditDocument
from .serializers import AuditDocumentSerializer


class AuditDocumentList(generics.ListCreateAPIView):
    queryset = AuditDocument.objects.all()
    serializer_class = AuditDocumentSerializer

class AuditDocument(generics.RetrieveUpdateDestroyAPIView):
    queryset = AuditDocument.objects.all()
    serializer_class = AuditDocumentSerializer
