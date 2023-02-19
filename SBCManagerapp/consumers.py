from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer

class ChatConsumer(WebsocketConsumer):

    def websocket_connect(self, message):
        self.accept()

    def websocket_receive(self, message):
        self.send(text_data='OK')       # 返回给客户端的消息

    def websocket_disconnect(self, message):
        raise StopConsumer()
