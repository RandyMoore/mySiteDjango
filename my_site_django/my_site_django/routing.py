from channels.routing import route
from government_audit.consumers import named_entity_search

channel_routing = [
    route("websocket.receive", named_entity_search, path="^/namedEntitySearch$"),
]