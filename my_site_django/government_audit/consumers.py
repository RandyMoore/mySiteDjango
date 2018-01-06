'''
Consumers for websocket traffic

The consumer runs on a single thread processing requests off a message queue.  Django is NOT asyncio enabled.
The received messages are processed asynchronously in a 2nd thread.
'''
import aiohttp
import asyncio
import json
from threading import Thread

session = aiohttp.ClientSession()
loop = asyncio.get_event_loop()


async def check_url(message):
    un_checked_url = json.loads(message.content['text'])
    try:
        async with session.head(un_checked_url['url'], allow_redirects=True, timeout=10) as url_head_response:
            message_response = {
                'id': un_checked_url['id'],
                'isActive': url_head_response.status == 200,
                'url': str(url_head_response.url)}

            message.reply_channel.send({
                "text": json.dumps(message_response),
            })

    except aiohttp.client_exceptions.ClientConnectorError as e:
        print(f"Received ClientConnectorError {e}")


def get_year_set(message):
    message_data = json.loads(message.content['text'])
    years = message_data['years']
    # Django ORM doesn't allow annotation after a union
    # https://code.djangoproject.com/ticket/26019
    #  which is required here to count how many documents each named entity appears in.
    # To keep the code simple and efficient we normalize 'before2014' to be year values in the
    #  set of years to include in the query (to avoid a union with queryset asking for year < 2014)
    # 1978 is the year of the earliest document:
    #   SELECT DISTINCT EXTRACT(year from "publication_date") AS year
    #   FROM government_audit_auditdocument
    #   ORDER BY year
    #   LIMIT 1
    if 'before2014' in years:
        years.remove('before2014')
        years.extend(range(1978, 2014))

    if not years:
        years = list(range(1978, 2018))

    return years


async def get_remaining_top_named_entities(message, document_qs=None):
    from django.db.models import Count
    from .models import NamedEntity
    message_data = json.loads(message.content['text'])
    selected_entities = message_data['selectedEntities']
    offset = message_data['entityOffset']

    years = get_year_set(message)

    qs = NamedEntity.objects
    if years:
        qs = qs.filter(document__publication_date__year__in=years)

    # Only include entities already in the documents containing all of the entities already selected.
    if document_qs:
        qs = qs.filter(document__in=document_qs)

    qs = qs.exclude(name__in=selected_entities).values('name').annotate(numDocs=Count('document'))

    total_size = qs.count()
    results = list(qs.order_by('-numDocs')[offset:offset + 10])

    return results, selected_entities, offset, total_size


async def named_entity_document_search(message):
    from .models import AuditDocument

    message_data = json.loads(message.content['text'])
    named_entities = message_data['selectedEntities']
    document_offset = message_data['documentOffset']
    years = get_year_set(message)

    document_qs = None
    if named_entities:
        document_qs = AuditDocument.objects.filter(publication_date__year__in=years)
        for named_entity in named_entities:
            document_qs = document_qs.filter(named_entities__name__in=[named_entity])

    top_entities, selected_entities, entity_offset, entity_total_size = \
        await get_remaining_top_named_entities(message, document_qs)

    document_results = [
        [str(doc.id), {
            'title': doc.title,
            'url': doc.url,
            'date': str(doc.publication_date)}
        ] for doc in
        document_qs[document_offset:document_offset+10]] if document_qs else []

    message_response = {
        'selectedEntities': named_entities,
        'topEntities': top_entities,
        'entityResultsSize': entity_total_size,
        'entityOffset': entity_offset,
        'documentResults': document_results,
        'documentResultsSize': document_qs.count() if document_qs else 0,
        'documentOffset': document_offset
    }

    message.reply_channel.send({
        "text": json.dumps(message_response),
    })


def run_async_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever() # this is a blocking call, needs to be in a separate thread.


def verify_url(message):
    loop.call_soon_threadsafe(asyncio.async, check_url(message))


def named_entity_search(message):
    loop.call_soon_threadsafe(asyncio.async, named_entity_document_search(message))


t = Thread(target=run_async_loop, args=(loop,), daemon=True)
t.start()