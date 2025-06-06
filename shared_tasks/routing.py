from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/shared-tasks/', consumers.SharedTaskConsumers.as_asgi()),
]