import asyncio

import functools
import requests
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from psycopg2 import Error

from .models import AuditDocument


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

            loop = asyncio.new_event_loop()
            urlHeadResponses = loop.run_until_complete(checkUrls([m.url for m in matches]))

            results = [{'title': m.title,
                        'url': head.url if head.ok else m.url,
                        'date': m.publication_date,
                        'rank': m.rank,
                        'urlActive': head.ok}
                       for m, head in  zip(matches, urlHeadResponses)]

            return JsonResponse({'results': results, 'offset': offset, 'size': size, 'query': query})
        except Error as e:
            return JsonResponse({'error': e.pgerror})

    else:
        return render(request, 'government_audit/audit_search.html', {'props': {}})


# Check if urls are available in parallel.  TODO: do this after send initial response back to client.
async def checkUrls(urlList):
    loop = asyncio.get_event_loop()
    head_futures = [
        loop.run_in_executor(
            None,
            functools.partial(
                requests.head,
                url,
                allow_redirects=True
            )
        )
        for url in urlList
    ]
    responses = [response for response in await asyncio.gather(*head_futures)]
    return responses

    responses = []
    for url in urlList:
        responses.append(await session.head(url))
    return session.run(responses)
