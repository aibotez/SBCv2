import os,json,time
import hashlib
from SBCShareapp.models import SBCShare
from SBC import GetUserPath

class ShareManage():
    def __init__(self):
        pass

    def string_to_md5(self,string):
        md5_val = hashlib.md5(string.encode('utf8')).hexdigest()
        return md5_val
    def CreatShareUrl(self,ShareFileInfo,LoginRes,req):
        userEmail = LoginRes['useremail']
        # getuserpath = GetUserPath.GetUserPath()
        # paths = getuserpath.userpath(req, LoginRes)
        ShareFileInfoMd5 = self.string_to_md5(userEmail+json.dumps(ShareFileInfo))
        if SBCShare.objects.filter(ShareLink=ShareFileInfoMd5).exists():
            return 'exists'
        curtime = int(time.time())
        SBCShare.objects.create(ShareLink=ShareFileInfoMd5, ShareFileInfo=json.dumps(ShareFileInfo),
                                useremail=userEmail,password=ShareFileInfo['SharePass'], ShareTime=curtime, toUser='0')
        return ShareFileInfoMd5

