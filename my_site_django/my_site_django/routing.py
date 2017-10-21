from channels.routing import route
from government_audit.consumers import named_entity, verify_url

channel_routing = [
    route("websocket.receive", verify_url, path="^/verifyUrl"),
    route("websocket.receive", named_entity, path="^/namedEntity")
]