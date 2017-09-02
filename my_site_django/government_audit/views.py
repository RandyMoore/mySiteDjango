from django.shortcuts import render
from rest_framework import generics

from .models import AuditDocument
from .serializers import AuditDocumentSerializer

# Django
def search(request):
    return render(request, 'government_audit/audit_search.html', {'props': {}})

# REST API
class AuditDocumentList(generics.ListCreateAPIView):
    queryset = AuditDocument.objects.all()
    serializer_class = AuditDocumentSerializer
