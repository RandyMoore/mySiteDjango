from channels.routing import route
from government_audit.consumers import named_entity_search, verify_url

channel_routing = [
    route("websocket.receive", verify_url, path="^/verifyUrl$"),
    route("websocket.receive", named_entity_search, path="^/namedEntitySearch$"),
]