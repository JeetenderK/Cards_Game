from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    path('JorPatti_WebApp/', consumers.JorPatti_WebAppConsumer),
    #re_path(r'ws/JorPatti/$', consumers.JorPatti_WebAppConsumer),
]