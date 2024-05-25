from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/videocall/(?P<group_id>\d+)/$", consumers.VideoCallConsumer.as_asgi()),
]
