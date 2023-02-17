from SBCManagerapp import models as SBCManagemodels
from Usersapp.models import User
import json
class Manage():
    def __init__(self):
        pass

    def GetSerInfo(self):
        Info = SBCManagemodels.SBCManager.objects.all()
        if Info:
            info = {}
            info['SBCStockSize'] = Info[0].SBCStockSize
            info['FileStock'] = Info[0].FileStock
            info['UserStock'] = Info[0].UserStock
            return info
        return 0

    def ModCap(self,request):

        info = request.POST
        GetSerInfo = self.GetSerInfo()
        Total = GetSerInfo['SBCStockSize']
        if int(info['ModCap']) > Total:
            info['ModCap'] = Total
        user = info['user']
        ModCap = int(info['ModCap'])*1024*1024*1024
        Userfo = User.objects.get(username=user)
        Userfo.totalcapacity = ModCap
        Userfo.save()
