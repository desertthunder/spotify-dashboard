"""Channel Routing."""

from django.urls import path

from live.consumers import NotificationConsumer

websocket_urlpatterns = [path("ws/notifications", NotificationConsumer.as_asgi())]