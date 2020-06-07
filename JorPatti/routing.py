from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import JorPatti_WebApp.routing

application = ProtocolTypeRouter({
    # Empty for now (http -> django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            JorPatti_WebApp.routing.websocket_urlpatterns
        )
    ),
})