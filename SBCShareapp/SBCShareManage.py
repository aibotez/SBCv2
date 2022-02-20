import os,json,time,random
import hashlib
from SBCShareapp.models import SBCShare
from SBC import GetUserPath

class ShareManage():
    def __init__(self):
        self.RangeNums = []
        self.intRandomList()
    def intRandomList(self):
        RangeNums0 = [i for i in range(10)]
        RangeNums1 = [i for i in range(65, 91)]
        RangeNums2 = [i for i in range(97, 123)]
        self.RangeNums = RangeNums0 + RangeNums1 + RangeNums2
    def CreatShareCode(self):
        ShareCode = ''
        for i in range(4):
            char=random.choice(self.RangeNums)
            if char <10:
                chari = str(char)
            else:
                chari = chr(char)
            ShareCode = ShareCode+chari
        return ShareCode

    def string_to_md5(self,string):
        md5_val = hashlib.md5(string.encode('utf8')).hexdigest()
        return md5_val
    def CreatShareUrl(self,ShareFileInfo,LoginRes,req):
        userEmail = LoginRes['useremail']
        ShareFileInfo['useremail'] = userEmail
        # getuserpath = GetUserPath.GetUserPath()
        # paths = getuserpath.userpath(req, LoginRes)
        ShareFileInfostr = json.dumps(ShareFileInfo)

        if SBCShare.objects.filter(ShareFileInfo=ShareFileInfostr).exists() :
            ShareData = SBCShare.objects.get(ShareFileInfo=ShareFileInfostr)
            if ShareData.useremail == userEmail:
                return ShareData.ShareLink
        # ShareFileInfoMd5 = self.string_to_md5(userEmail+json.dumps(ShareFileInfo))
        # if SBCShare.objects.filter(ShareLink=ShareFileInfoMd5).exists():
        #     return ShareFileInfoMd5
        curtime = int(time.time())
        ShareCode = self.CreatShareCode()
        SBCShare.objects.create(ShareLink=ShareCode, ShareFileInfo=json.dumps(ShareFileInfo),
                                useremail=userEmail,password=ShareFileInfo['SharePass'], ShareTime=curtime, toUser='0')
        return ShareCode

