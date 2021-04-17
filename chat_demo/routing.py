from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from chat.consumers import EchoConsumer, ChatConsumer
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
        re_path(r'ws/chat/(?P<username>\w+)/$', ChatConsumer.as_asgi()),
        re_path(r'^ws/chat/$', EchoConsumer.as_asgi() ),
        ])
    ),
})


