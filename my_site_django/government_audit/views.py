from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics
from psycopg2 import Error

from .models import AuditDocument
from .serializers import AuditDocumentSerializer


# Django
def search(request):
    query = request.GET['query'] if 'query' in request.GET else None
    if query:
        query_func = {
            'plain': 'plainto_tsquery',
            'phrase': 'phraseto_tsquery',
            'raw': 'to_tsquery'
        }

        # TODO: Figure out how to express @@ operator without resorting to raw SQL
        try:
            text_query = f"{ query_func[request.GET['parser']] }('{ query }')"

            # TODO: Use sockets instead to retain state server side.
            with connection.cursor() as cursor:
                cursor.execute(f'SELECT count(1) FROM government_audit_auditdocument WHERE lexemes @@ { text_query } ')
                size = cursor.fetchone()[0]

            offset = int(request.GET['offset'])
            limit = int(request.GET['limit'])

            matches = AuditDocument.objects.raw(f'''
            SELECT id, title, publication_date, url, ts_rank_cd(lexemes, { text_query }) AS rank
            FROM government_audit_auditdocument
            WHERE lexemes @@ { text_query }
            ORDER BY rank, id desc
            LIMIT { limit } OFFSET { offset } ''')

            results = [{'title': m.title, 'url': m.url, 'date': m.publication_date, 'rank': m.rank} for m in matches]

            return JsonResponse({'results': results, 'size': size, 'query': query})
        except Error as e:
            return JsonResponse({'error': e.pgerror})

    else:
        return render(request, 'government_audit/audit_search.html', {'props': {}})


# REST API
class AuditDocumentList(generics.ListCreateAPIView):
    queryset = AuditDocument.objects.all()
    serializer_class = AuditDocumentSerializer
