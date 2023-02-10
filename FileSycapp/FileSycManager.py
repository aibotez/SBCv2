from SBC import GetUserPath
import os,hashlib,time
from SBC import UserManage
from UserFileRecordapp import UserFileRecordManage
from UserFileRecordapp import models
from django.db.models import Q




def str_trans_to_md5(src):
    src = src.encode("utf-8")
    myMd5 = hashlib.md5()
    myMd5.update(src)
    myMd5_Digest = myMd5.hexdigest()
    return myMd5_Digest
class FileSycManager():
    def __init__(self):
        self.getuserpath = GetUserPath.GetUserPath()
    def GetFileMd5(self,filename):
        if not os.path.isfile(filename):
            return
        myhash = hashlib.md5()
        f = open(filename,"rb")
        while True:
            b = f.read(2*1024*1024)
            if not b:
                break
            myhash.update(b)
        f.close()
        return myhash.hexdigest()
    def GetFilesAll(self,useremail,path):
        Serpath = self.getuserpath.getuserserpath(useremail,path)
        Serpathdir = os.path.dirname(Serpath)
        files = {}
        FindFile = models.UserFileRecord.objects.filter(Q(useremail=useremail) & Q(FilePath__icontains=path))
        for i in FindFile:
            FileInfo = {}
            FileInfo['fepath'] = i.FilePath
            FileInfo['size'] = i.FileSize
            date = time.mktime(time.strptime(i.FileModTime, '%Y-%m-%d %H:%M'))
            FileInfo['date'] = date
            FileInfo['filemd5'] = i.FileMd5
            FileInfo['fapath1'] = Serpath.replace(Serpathdir,'')
            files[str_trans_to_md5(i.FilePath)] = FileInfo
        return files



    def checkFile(self,fileinfo):
        feMd5 = fileinfo['LoMD5']
        RoFilePath = fileinfo['RoFilePath']
        RoFileFaPath = fileinfo['RoFileFaPath']
        FileName = fileinfo['FileName']
        useremail = fileinfo['useremail']
        dst = self.getuserpath.getuserserpath(useremail,RoFileFaPath)
        exist = 0
        FileStart = 0
        if os.path.exists(dst+'/'+feMd5):
            exist = 1
            FileStart = os.path.getsize(dst+'/'+feMd5)
        FileCheck = {'exist': exist,'FileStart': FileStart}
        return FileCheck

    def UpFile(self,fileinfo,file_obj):
        feMd5 = fileinfo['LoMD5']
        RoFilePath = fileinfo['RoFilePath']
        RoFileFaPath = fileinfo['RoFileFaPath']
        FileName = fileinfo['FileName']
        FileSeekStart = fileinfo['FileSeekStart']
        useremail = fileinfo['useremail']
        dst = self.getuserpath.getuserserpath(useremail, RoFileFaPath)
        if not os.path.isdir(dst):
            os.makedirs(dst)
        with open(dst+'/'+feMd5, "ab") as f:
            for chunk in file_obj.chunks(chunk_size=2 * 1024 * 1024):
                f.write(chunk)
        if feMd5 == self.GetFileMd5(dst+'/'+feMd5):
            os.rename(dst+'/'+feMd5,dst+'/'+FileName)
            usermange = UserManage.usermange()
            usermange.AddUsedCap(useremail, os.path.getsize(dst+'/'+FileName))
            userfilerecordmanage = UserFileRecordManage.userfilerecordmanage()
            userfilerecordmanage.AddNewRecord(useremail,RoFileFaPath + '/' + FileName, feMd5)
            return 1
        else:
            os.remove(dst+'/'+feMd5)
            return 0