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
    unCheckedUrl = json.loads(message.content['text'])
    async with session.head(unCheckedUrl['url'], allow_redirects=True, timeout=10) as urlHeadResponse:
        message_response = {
            'id': unCheckedUrl['id'],
            'isActive': urlHeadResponse.status == 200,
            'url': str(urlHeadResponse.url)}

        message.reply_channel.send({
            "text": json.dumps(message_response),
        })


def verify_url(message):
    loop.call_soon_threadsafe(asyncio.async, check_url(message))

t = Thread(target=run_url_checker, args=(loop,))
t.start()