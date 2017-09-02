from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics

from .models import AuditDocument
from .serializers import AuditDocumentSerializer


# Django
def search(request):
    query = request.GET['query'] if 'query' in request.GET else None
    if query:
        # TODO: Figure out how to express @@ expression without raw SQL
        matches = AuditDocument.objects.raw(f'''
        SELECT id, title, publication_date, url
        FROM government_audit_auditdocument
        WHERE lexemes @@ plainto_tsquery('{ query }')
        LIMIT 10''')

        results = [{'title': m.title, 'url': m.url} for m in matches]

        return JsonResponse({'results': results, 'query': query})
    else:
        return render(request, 'government_audit/audit_search.html', {'props': {}})


# REST API
class AuditDocumentList(generics.ListCreateAPIView):
    queryset = AuditDocument.objects.all()
    serializer_class = AuditDocumentSerializer
