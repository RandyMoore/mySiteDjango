'''
Consumers for websocket traffic

The consumer runs on a single thread processing requests off a message queue.  Django is NOT asyncio enabled.
The received messages are processed asynchronously in a 2nd thread.
'''
import json
import aiohttp
import asyncio
from threading import Thread

session = aiohttp.ClientSession()
loop = asyncio.get_event_loop()


def run_url_checker(loop):
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


t = Thread(target=run_url_checker, args=(loop,), daemon=True)
t.start()