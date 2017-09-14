from channels.routing import route
from government_audit.consumers import verify_url

channel_routing = [
    route("websocket.receive", verify_url, path="^/verifyUrl")
]