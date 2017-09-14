import json
import requests


def verify_url(message):
    unCheckedUrl = json.loads(message.content['text'])

    urlHeadResponse = requests.head(unCheckedUrl['url'], allow_redirects=True)
    response = {
        'id': unCheckedUrl['id'],
        'isActive': urlHeadResponse.ok,
        'url': urlHeadResponse.url}

    message.reply_channel.send({
        "text": json.dumps(response),
    })

