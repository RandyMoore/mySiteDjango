from django.conf import settings
from django.db import connection
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
import json
from psycopg2 import Error

from .models import AuditDocument


def search(request):
    query = request.GET['query'] if 'query' in request.GET else None
    if query:
        if hasattr(settings, 'MAX_QUERY_LENGTH') and len(query) > settings.MAX_QUERY_LENGTH:
            return HttpResponseBadRequest(f"Query length is limited to { settings.MAX_QUERY_LENGTH } characters.")

        query_func = {
            'plain': 'plainto_tsquery',
            'phrase': 'phraseto_tsquery',
            'raw': 'to_tsquery'
        }

        try:
            text_query = f"{ query_func[request.GET['parser']] }('{ query }')"

            years = json.loads(request.GET['years'])
            year_clauses = []
            if 'before2014' in years:
                years.remove('before2014')
                year_clauses.append('EXTRACT(year FROM government_audit_auditdocument.publication_date) < 2014')

            if years:
                year_clauses.append(f"EXTRACT(year FROM government_audit_auditdocument.publication_date) IN ({ ', '.join(years) })")

            finalYearClause = ''
            if len(year_clauses) == 2:
                finalYearClause = 'AND (' + year_clauses[0] + ' OR ' + year_clauses[1] + ')'
            elif len(year_clauses) == 1:
                finalYearClause = 'AND ' + year_clauses[0]

            # TODO: Use sockets instead to retain state server side.
            with connection.cursor() as cursor:
                cursor.execute(f'SELECT count(1) FROM government_audit_auditdocument WHERE lexemes @@ { text_query } { finalYearClause } ')
                size = cursor.fetchone()[0]

            offset = int(request.GET['offset'])
            limit = int(request.GET['limit'])

            matches = AuditDocument.objects.raw(f'''
            SELECT id, title, publication_date, url, url_active, ts_rank_cd(lexemes, { text_query }) AS rank
            FROM government_audit_auditdocument
            WHERE lexemes @@ { text_query }
            { finalYearClause }
            ORDER BY rank, id desc
            LIMIT { limit } OFFSET { offset } ''')

            # Return a list of lists, each nested list has [key, value].
            # This allows us to create a Javascript Immutable.OrderedMap directly
            results = [
                [str(m.id), {
                    'title': m.title,
                    'url': m.url,
                    'url_active': m.url_active,
                    'date': m.publication_date,
                    'rank': m.rank}]
                for m in matches]

            return JsonResponse({'documentResults': results,
                                 'documentOffset': offset,
                                 'documentResultsSize': size})
        except Error as e:
            return JsonResponse({'error': e.pgerror})

    else:
        return render(request, 'government_audit/audit_search.html', {'props': {}})


