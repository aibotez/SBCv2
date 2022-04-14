from django.http import StreamingHttpResponse,FileResponse
from django.utils.encoding import escape_uri_path
import os,hashlib

from Usersapp.models import User
from FileDownUpapp import models
from SBC import GetUserPath
from SBC import UserManage
from UserFileRecordapp import UserFileRecordManage




class MakeLink():
    def __init__(self):
        # self.FilesStock = r'D:\documents\GitStock\SBCuserTest\FilesStock'
        self.FilesStock = r'C:\SBC\SBCStock'

    def mklk(self,dst,srcfename,dstfename):
        # dstDirs = r'D:\documents\GitStock\SBCuserTest\2290227486@qq.com'
        fe = dst+'/'+dstfename
        if os.path.exists(fe):
            os.remove(fe)
        os.symlink(self.FilesStock+'/'+srcfename,fe)




class FileUp():
    def __init__(self):
        self.FilesInfo=None
        # self.FilesStock = 'D:/documents/GitStock/SBCuserTest/FilesStock/'
        # self.FileServerHome = 'D:/documents/GitStock/SBCuserTest/'
        self.FilesStock = 'C:/SBC/SBCStock/'
        self.FileServerHome = 'C:/SBC/SBCUsers/'
        self.getuserpath = GetUserPath.GetUserPath()

    def GetFileMd5(self,filename):
        if not os.path.isfile(filename):
            return
        myhash = hashlib.md5()
        f = open(filename,"rb")
        while True:
            b = f.read(8096)
            if not b:
                break
            myhash.update(b)
        f.close()
        return myhash.hexdigest()

    def UpfileCheck(self,redit,useremail):
        feMd5 = redit['FileMd5']
        # print(feMd5)
        userpath = redit['CurPath']
        if not redit['webkitRelativePath'] =='':
            userpath = userpath + redit['webkitRelativePath'].replace(redit['FileName'],'')
        if models.FilesStock.objects.filter(FileMd5=feMd5).exists():
            dst = self.getuserpath.getuserserpath(useremail,userpath)
            if not os.path.isdir(dst):
                os.makedirs(dst)
            dstfename = redit['FileName']
            srcfename = models.FilesStock.objects.get(FileMd5=feMd5).FileName
            lk = MakeLink()
            lk.mklk(dst,srcfename,dstfename)
            usermange = UserManage.usermange()
            usermange.AddUsedCap(useremail,os.path.getsize(self.FilesStock + redit['FileName']))


            dstuserpath = dst + redit['FileName']
            userfilerecordmanage = UserFileRecordManage.userfilerecordmanage()
            userfilerecordmanage.AddNewRecord(useremail,dstuserpath)

            return {'exist':1}
        else:
            FileStart = 0
            if feMd5 in os.listdir(self.FilesStock):
                FileStart = os.path.getsize(self.FilesStock+feMd5)
                # if FileStart == redit['FileSize']:
                #     if feMd == self.GetFileMd5(filename):
            FeInfo = {
                'exist':0,
                'FileStart':FileStart
            }
            return FeInfo

    def Upfile(self,redit,useremail,file_obj):
        feMd5 = redit['FileMd5']
        userpath = redit['CurPath']
        userpath = redit['CurPath']
        if not redit['webkitRelativePath'] =='':
            userpath = userpath + redit['webkitRelativePath'].replace(redit['FileName'],'')

        with open(self.FilesStock + feMd5, "ab") as f:
            # f.seek(0,2)
            for chunk in file_obj.chunks(chunk_size=2 * 1024 * 1024):
                f.write(chunk)
        # print(redit['FileSize'],os.path.getsize(self.FilesStock + feMd5))
        # print(type(redit['isLastChunk']))
        # print(self.FilesStock + redit['FileName'])
        if (int(redit['isLastChunk'])):
            if os.path.exists(self.FilesStock + redit['FileName']):
                os.remove(self.FilesStock + redit['FileName'])
            os.rename(self.FilesStock + feMd5,self.FilesStock + redit['FileName'])
            dst = self.getuserpath.getuserserpath(useremail,userpath)


            if not os.path.isdir(dst):
                os.makedirs(dst)
            dstfename = redit['FileName']
            srcfename = redit['FileName']
            lk = MakeLink()
            lk.mklk(dst,srcfename,dstfename)
            models.FilesStock.objects.create(FileMd5=feMd5, FileName=srcfename,FilePath=self.FilesStock + srcfename)
            usermange = UserManage.usermange()
            usermange.AddUsedCap(useremail,os.path.getsize(self.FilesStock + redit['FileName']))

            dstuserpath = dst + redit['FileName']
            userfilerecordmanage = UserFileRecordManage.userfilerecordmanage()
            userfilerecordmanage.AddNewRecord(useremail, dstuserpath)

        #
        # if models.FilesStock.objects.filter(FileMd5=feMd5).exists():
        #     dst =self.FileServerHome+useremail
        #     dstfename = file_obj.name
        #     srcfename = models.FilesStock.objects.filter(FileMd5=feMd5).FileName
        #     lk = MakeLink()
        #     lk.mklk(dst,srcfename,dstfename)
        # else:
        #     with open(self.FilesStock + file_obj.name, "wb") as f:
        #         for chunk in file_obj.chunks(chunk_size=2 * 1024 * 1024):
        #             f.write(chunk)
        #     dst =self.FileServerHome+useremail
        #     dstfename = file_obj.name
        #     srcfename = file_obj.name
        #     lk = MakeLink()
        #     lk.mklk(dst,srcfename,dstfename)
        #     models.FilesStock.objects.create(FileMd5=feMd5, FileName=srcfename,FilePath=self.FilesStock + srcfename)

class FileDU():
    def __init__(self):
        pass

    def file_iterator(self,file_name, chunk_size=20 * 1024 * 1024):
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    def Down(self,FileInfo):

        the_file_name = FileInfo['fename']
        the_file_path = FileInfo['fepath']
        # print(the_file_name,the_file_path)
        #response = FileResponse(file_iterator(the_file_name))
        response = StreamingHttpResponse(self.file_iterator(the_file_path))
        response = FileResponse(response)
        response['Content-Type'] = 'application/octet-stream'
        response['content-length'] = os.path.getsize(the_file_path)
        #response['Content-Disposition'] = 'attachment;filename="{0}"'.format(wjname)
        response["Content-Disposition"] = "attachment; filename*=UTF-8''{}".format(escape_uri_path(the_file_name))
        return response