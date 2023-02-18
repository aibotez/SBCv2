import os

from SBCManagerapp import models as SBCManagemodels
from Usersapp.models import User
from UserFileRecordapp.models import UserFileRecord
from FileDownUpapp.models import FilesStock
from pack import CommMode
import json
from SBC import GetUserPath
from django.db.models import Q
from SBC import UserManage




class Manage():
    def __init__(self):
        self.ComTol = CommMode.ComTol()

    def DelStockFiles(self,req):
        info = json.loads(req.body)
        Files = info['Files']
        Serinfo = self.GetSerInfo()
        getuserpath = GetUserPath.GetUserPath()
        usermange = UserManage.usermange()
        for i in Files:
            Path = Serinfo['FileStock'] + i['MD5'] + '#' + i['FileName']
            if 'linkuser' in i:
                AllUserFIles = UserFileRecord.objects.filter(FileMd5 = i['MD5'])
                for va in AllUserFIles.values():
                    info = va
                    path = info.FilePath
                    useremail = info.useremail
                    userPath = getuserpath.getuserserpath(useremail, path)
                    DirsSize = os.path.getsize(userPath)
                    os.remove(userPath)
                    usermange.DelUsedCap(useremail, DirsSize)
                    os.remove(userPath)
            try:
                os.remove(Path)
            except:
                pass





    def GetFilesAll(self):
        AllUserFIles = UserFileRecord.objects.all()
        AllStockFiles = FilesStock.objects.all()
        # allstockFiles = [{'MD5':i.FileMd5,'FileName':i.FileName,'FilePath':i.FilePath} for i in AllStockFiles]
        # alluserFiles = [{'MD5':i.FileMd5,'FileName':i.FileName,'FileType':i.FileType,'UserEmail':i.useremail,'FileSize':i.FileSize} for i in AllUserFIles]

        alluserFiles = {}
        for i in AllUserFIles:
            alluserFiles[i.FileMd5] = {'MD5':i.FileMd5,'FileType':i.FileType,'UserEmail':i.useremail,'FileSize':i.FileSize}
        FileNoUser = []
        allstockFiles = []
        for i in AllStockFiles:
            FileName = i.FileName.replace(i.FileMd5+'#','')
            if i.FileMd5 in alluserFiles:
                info = {'linkuser':alluserFiles[i.FileMd5],'MD5':i.FileMd5,'FileName':FileName,'FileType':alluserFiles[i.FileMd5]['FileType'],'FileSize':alluserFiles[i.FileMd5]['FileSize'],'FileSizestr':self.ComTol.size_format(alluserFiles[i.FileMd5]['FileSize'])}
            else:
                if os.path.exists(i.FilePath):
                    FileSize = os.path.getsize(i.FilePath)
                    info = {'MD5': i.FileMd5, 'FileName': FileName, 'FileType': self.ComTol.GetImgConPath(i.FilePath), 'FileSize': FileSize,'FileSizestr':self.ComTol.size_format(FileSize)}
                else:
                    info = {}
                FileNoUser.append(info)
            allstockFiles.append(info)
        return {'all':allstockFiles,'NoUser':FileNoUser}


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
        ModCap = 1024*(int(info['ModCap'])*1024*1024*1024)/1000
        Userfo = User.objects.get(username=user)
        Userfo.totalcapacity = ModCap
        Userfo.save()
