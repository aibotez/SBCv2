import json

from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from SBCManagerapp import models as SBCManagemodels
from SBCManagerapp import Man


def verifylogin(request):
    cookies = request
    LoginRes = {'res': 1, 'useremail': ''}
    if 'coks' in cookies:
        cok = cookies['coks']
        cok = cok.split(';')[-1].replace(' ','')
        usefo = cok.split('auth:')
        if SBCManagemodels.SBCManager.objects.filter(SBCManageEmail=usefo[0]).exists():
            if SBCManagemodels.SBCManager.objects.get(SBCManageEmail=usefo[0]).SBCUserPass0 == usefo[1]:
                LoginRes['res'] = 0
                LoginRes['useremail'] = usefo[0]
                return LoginRes
    return LoginRes

class ChatConsumer(WebsocketConsumer):

    def websocket_connect(self, message):
        self.accept()

    def websocket_receive(self, message):


        info = json.loads(message['text'])
        LoginRes = verifylogin(info)
        if LoginRes['res']:
            self.send(text_data=json.dumps({'res':0}))
        if 'SerInfos' in info:
            if 'DiskIndex' in info:

                info = Man.Manage().GetSerInfos(1)
            else:
                info = Man.Manage().GetSerInfos()
        elif 'DiskHealthInfo' in info:
            if 'DiskIndex' in info:
                info = Man.Manage().GetDiskInfo(1)
            else:
                info = Man.Manage().GetDiskInfo(0)
        elif 'ModSBCstock' in info:
            ModSBCstock = info['ModSBCstock']
            info = Man.Manage().ModSBCstock(ModSBCstock)
        elif 'GetMountDisks' in info:
            info = {'data':Man.Manage().GetDiskParinfo()}

        info['res'] = 1
        self.send(text_data=json.dumps(info))       # 返回给客户端的消息

    def websocket_disconnect(self, message):
        raise StopConsumer()
