"""
ASGI config for SBC project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

# import os
#
# from django.core.asgi import get_asgi_application
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SBC.settings')
#
# application = get_asgi_application()



import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from . import routing     # 这个文件后续会说，你先写上。

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SBC.settings')
# application = get_asgi_application()  # 注释掉原来的application

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),     # http走Django默认的asgi
        "websocket": URLRouter(routing.websocket_urlpatterns),         # websocket走channels
    }
)