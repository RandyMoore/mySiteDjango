from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics

from .models import AuditDocument
from .serializers import AuditDocumentSerializer


# Django
def search(request):
    query = request.GET['query'] if 'query' in request.GET else None
    if query:
        return JsonResponse({'results': [{'title': 'The Greatest Awesome', 'url': 'http://fakeone.com'}]})
    else:
        return render(request, 'government_audit/audit_search.html', {'props': {}})


# REST API
class AuditDocumentList(generics.ListCreateAPIView):
    queryset = AuditDocument.objects.all()
    serializer_class = AuditDocumentSerializer
