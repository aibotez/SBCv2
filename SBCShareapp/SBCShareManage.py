import os,json,time,random
import hashlib
from SBCShareapp.models import SBCShare
from SBC import GetUserPath
from SBC import GetUserPath


def size_format(size):
    if size < 1024:
        return '%i' % size + 'B'
    elif 1024 <= size < 1024*1024:
        return '%.1f' % float(size/1024) + 'KB'
    elif 1024*1024 <= size < 1024*1024*1024:
        return '%.1f' % float(size/(1024*1024)) + 'MB'
    elif 1024*1024*1024 <= size < 1024*1024*1024*1024:
        return '%.1f' % float(size/(1024*1024*1024)) + 'GB'
    elif 1024*1024*1024*1024 <= size:
        return '%.1f' % float(size/(1024*1024*1024*1024)) + 'TB'
class ShareManage():
    def __init__(self):
        self.RangeNums = []
        self.intRandomList()
        self.getuserpath = GetUserPath.GetUserPath()
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
    def CreatShareUrl(self,ShareFileInfo,LoginRes,CurUrl):
        userEmail = LoginRes['useremail']
        ShareFileInfo['useremail'] = userEmail
        shareCurPath = ShareFileInfo['ShareFile'][0]['fepath']
        if shareCurPath[-1] == '/':
            shareCurPath = shareCurPath[0:-1]
        shareFaPath = shareCurPath.split('/')
        del shareFaPath[0]
        del shareFaPath[0-1]
        shareFaPath = '/'+'/'.join(shareFaPath)
        ShareFileInfo['shareFaPath'] = shareFaPath
        for i in range(len(ShareFileInfo['ShareFile'])):
            ShareFileInfo['ShareFile'][i]['fepath'] = ShareFileInfo['ShareFile'][i]['fepath'].replace(shareFaPath,'')

        # getuserpath = GetUserPath.GetUserPath()
        # paths = getuserpath.userpath(req, LoginRes)
        ShareFileInfostr = json.dumps(ShareFileInfo)

        if SBCShare.objects.filter(ShareFileInfo=ShareFileInfostr).exists():
            ShareData = SBCShare.objects.get(ShareFileInfo=ShareFileInfostr)
            if ShareData.useremail == userEmail:
                return 'http://'+CurUrl+'/?SBCShare='+ShareData.ShareLink
        # ShareFileInfoMd5 = self.string_to_md5(userEmail+json.dumps(ShareFileInfo))
        # if SBCShare.objects.filter(ShareLink=ShareFileInfoMd5).exists():
        #     return ShareFileInfoMd5
        curtime = int(time.time())
        ShareCode = self.CreatShareCode()
        SBCShare.objects.create(ShareLink=ShareCode, ShareFileInfo=json.dumps(ShareFileInfo),
                                useremail=userEmail,password=ShareFileInfo['SharePass'], ShareTime=curtime, toUser='0')
        return 'http://'+CurUrl+'/SBCShare/?SBCShare='+ShareCode

    def checksharexist(self,sharelink):
        if SBCShare.objects.filter(ShareLink=sharelink).exists():
            return 1
        return 0

    def GetShareOutTime(self,shartime,durtime):
        if '7天' in durtime or '周' in durtime:
            return shartime + 7*24*60*60
        elif '1天' in durtime:
            return shartime + 1 * 24 * 60 * 60
        elif '1个月' in durtime or '30天' in durtime:
            return shartime + 30 * 24 * 60 * 60
        elif '永久' in durtime:
            return shartime + 100 * 12 * 30 * 24 * 60 * 60

    def checksharetimeout(self,sharelink):
        ShareData = SBCShare.objects.get(ShareLink=sharelink)
        sharetime = ShareData.ShareTime
        shareinfo = json.loads(ShareData.ShareFileInfo)
        shareOuttime = self.GetShareOutTime(sharetime,shareinfo['ShareDateDur'])
        if shareOuttime < time.time():
            return None
        return shareinfo

    def ShareCheck(self,sharelink):
        if not self.checksharexist(sharelink):
            return '分享不存在'
        shareinfo = self.checksharetimeout(sharelink)
        if not shareinfo:
            return '分享已超时'
        SharePass = shareinfo['SharePass']
        if SharePass:
            return 'password'
        return 'pass'

    def getdate(self,fie):
        statbuf = os.stat(fie)
        date = time.strftime('%Y-%m-%d %H:%M', time.localtime(statbuf.st_mtime))
        # date= statbuf.st_mtime
        return date
    def GetShareInfo(self,sharelink,password=None):
        shareinfo = self.checksharetimeout(sharelink)
        SharePass = shareinfo['SharePass']
        if SharePass and password != SharePass:
            return 'passworderror'
        ShareFilesInfo = shareinfo['ShareFile']
        FilesInfo = []
        for i in ShareFilesInfo:
            size = -1
            big = '-'
            ShareFile = i
            userpath = shareinfo['shareFaPath']+i['fepath']
            SerPath = self.getuserpath.getuserserpath(shareinfo['useremail'], userpath)
            ShareFile['date'] = self.getdate(SerPath)
            if not i['isdir']:
                size = os.path.getsize(SerPath)
                big = size_format(size)
            ShareFile['size'] = size
            ShareFile['big'] = big
            FilesInfo.append(ShareFile)
        return FilesInfo


