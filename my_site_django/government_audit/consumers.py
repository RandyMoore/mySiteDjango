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


# Returns a list of up to 2 query sets of named entities for year selections [[before214],[2014|2015|...]]
async def get_named_entities_for_years(message_data):
    from .models import NamedEntity

    years = message_data['years']
    before2014 = False

    if 'before2014' in years:
        before2014 = True
        years.remove('before2014')

    # Union does not support later operations, keep QuerySets separate and combine final results.
    entities_qs = []
    if years:
        entities_qs.append(NamedEntity.objects.filter(document__publication_date__year__in=years))
    if before2014:
        entities_qs.append(NamedEntity.objects.filter(document__publication_date__year__lt=2014))
    if not years and not before2014:
        entities_qs.append(NamedEntity.objects.all())

    return entities_qs


async def get_most_frequent_remaining_named_entities(entities_years_qs, named_entities):
    from django.db.models import Count

    docs_with_named_entities = set()
    entities_with_docs_of_selected_entities_qs = entities_years_qs

    if named_entities:
        qs_with_docs_having_selected_named_entities = []
        for qs in entities_years_qs:
            docs_with_all_named_entities = set()
            for ne in named_entities:
                docs_with_ne = set([doc['document'] for doc in qs.filter(name=ne).values('document')])
                if docs_with_all_named_entities:
                    docs_with_all_named_entities = docs_with_all_named_entities & docs_with_ne  # docs that include this AND all past named entities
                else:
                    docs_with_all_named_entities = docs_with_ne
            qs_with_docs_having_selected_named_entities.append(qs.filter(document__in=docs_with_all_named_entities))
            docs_with_named_entities.update(docs_with_all_named_entities)
            entities_with_docs_of_selected_entities_qs = qs_with_docs_having_selected_named_entities

    top_entities_nested = [entities \
                           .exclude(name__in=named_entities)
                           .values('name') \
                           .annotate(numDocs=Count('document')) \
                           .order_by('-numDocs')[:10] \
                       for entities in entities_with_docs_of_selected_entities_qs]

    # Flatten the lest
    top_entities = [e for e_list in top_entities_nested for e in e_list]

    return docs_with_named_entities, entities_with_docs_of_selected_entities_qs, top_entities


async def merge_top_entities(top_entities):
    merged = []
    top_entities.sort(key=lambda e: e['name'])
    for e in top_entities:
        if not merged or merged[-1]['name'] != e['name']:
            merged.append(e)
        else:
            merged[-1]['numDocs'] += e['numDocs']

    top_entities = sorted(merged, key=lambda e: e['numDocs'], reverse=True)[:10]
    return top_entities


async def named_entity_search(message):
    from .models import AuditDocument

    message_data = json.loads(message.content['text'])
    named_entities = message_data['entityList']

    entities_years_qs = await get_named_entities_for_years(message_data)

    docs_with_named_entities, entities_with_docs_of_selected_entities_qs, top_entities = \
        await get_most_frequent_remaining_named_entities(entities_years_qs, named_entities)

    if len(entities_years_qs) > 1:  # Merge the results from 2 querysets (before2014 and 2014|2015|...)
        top_entities = await merge_top_entities(top_entities)

    offset = message_data['offset']
    results = [
        [str(doc.id), {
            'title': doc.title,
            'url': doc.url,
            'date': str(doc.publication_date)}
        ] for doc in AuditDocument.objects.filter(id__in=docs_with_named_entities)[offset:offset+10]]

    message_response = {
        'selectedEntities': named_entities,
        'topEntities': top_entities,
        'results': results,
        'size': len(docs_with_named_entities),
        'offset': offset
    }

    message.reply_channel.send({
        "text": json.dumps(message_response),
    })


def run_async_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever() # this is a blocking call, needs to be in a separate thread.


def verify_url(message):
    loop.call_soon_threadsafe(asyncio.async, check_url(message))


def named_entity(message):
    loop.call_soon_threadsafe(asyncio.async, named_entity_search(message))


t = Thread(target=run_async_loop, args=(loop,), daemon=True)
t.start()