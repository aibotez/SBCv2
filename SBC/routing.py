from channels.routing import ProtocolTypeRouter

# application = ProtocolTypeRouter({
#     # 暂时为空
# })

from django.urls import re_path
from SBCManagerapp import consumers          # 从chat这个app导入consumers，先写上，稍后会说。

# websocket的路由配置
websocket_urlpatterns = [
    # re_path("^room/(?P<group>\w+)", consumers.ChatConsumer.as_asgi()),
    re_path("getSerInfows/", consumers.ChatConsumer.as_asgi()),
]
