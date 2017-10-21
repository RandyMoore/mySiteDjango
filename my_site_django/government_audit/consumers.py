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


def run_async_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever() # this is a blocking call, needs to be in a separate thread.


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
        print(f"Received ClientConnectorError {e}, retrying in 1 second...")
        asyncio.get_event_loop().call_later(1, verify_url, message)


def verify_url(message):
    loop.call_soon_threadsafe(asyncio.async, check_url(message))

async def named_entity_search(message):
    from .models import AuditDocument, NamedEntity
    from django.db.models import Count

    message_data = json.loads(message.content['text'])

    years = message_data['years']
    before2014 = False
    if 'before2014' in years:
        before2014 = True
        years.remove('before2014')

    named_entities = message_data['entityList']

    # Union does not support later operations, keep QuerySets separate and combine final results.
    entities_qs = []

    if years:
        entities_qs.append(NamedEntity.objects.filter(document__publication_date__year__in=years))

    if before2014:
        entities_qs.append(NamedEntity.objects.filter(document__publication_date__year__lt=2014))

    if not years and not before2014:
        entities_qs.append(NamedEntity.objects.all())

    top_entities_qs = [ entities\
        .values('name')\
        .annotate(numDocs=Count('document'))\
        .order_by('-numDocs')[:10]\
        for entities in entities_qs ]

    top_entities = [e for e_list in top_entities_qs for e in e_list]

    if years and before2014:
        merged = []
        top_entities.sort(key=lambda e: e['name'])
        for e in top_entities:
            if not merged or merged[-1]['name'] != e['name']:
                merged.append(e)
            else:
                merged[-1]['numDocs'] += e['numDocs']

        top_entities = sorted(merged, key=lambda e: e['numDocs'], reverse=True)[:10]

    message_response = {
        'selectedEntities': named_entities,
        'topEntities': top_entities
    }

    message.reply_channel.send({
        "text": json.dumps(message_response),
    })

def named_entity(message):
    loop.call_soon_threadsafe(asyncio.async, named_entity_search(message))

t = Thread(target=run_async_loop, args=(loop,), daemon=True)
t.start()