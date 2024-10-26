"""ASGI config for server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter  # type: ignore
from channels.security.websocket import AllowedHostsOriginValidator  # type: ignore
from django.core.asgi import get_asgi_application

import browser.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            URLRouter(browser.routing.websocket_urlpatterns)
        ),
    }
)
