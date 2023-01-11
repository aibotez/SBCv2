from UserFileRecordapp import models
from SBC import FileType
from django.db.models import Q
import os,time
from SBC import GetUserPath

class userfilerecordmanage():
    def __init__(self):
        self.filetype = FileType.FileType()
        self.getuserpath = GetUserPath.GetUserPath()



    def getdate(self,fie):
        statbuf = os.stat(fie)
        date = time.strftime('%Y-%m-%d %H:%M', time.localtime(statbuf.st_mtime))
        # date= statbuf.st_mtime
        return date

    def AddNewRecord(self,useremail,path,feMd5):

        fetype = self.filetype.GetFileType(path)[0]

        # if models.UserFileRecord.objects.filter(FileMd5=feMd5).exists():
        FindFile = models.UserFileRecord.objects.filter(
            Q(useremail=useremail) & Q(FilePath=path))
        if FindFile.exists():
            FindFile = models.UserFileRecord.objects.get(FilePath = path)
            if FindFile.FileType == fetype:
                return
            FindFile.FileType = fetype
            FindFile.save()
            return

        dst = self.getuserpath.getuserserpath(useremail,path)
        # print(dst)
        data = self.getdate(dst)
        Fesize = os.path.getsize(dst)
        models.UserFileRecord.objects.create(FileSize=Fesize,FileModTime=data,FileMd5=feMd5,useremail = useremail,FileType = fetype,FilePath = path,Expansion='')

    # models.FilesStock.objects.create(FileMd5=feMd5, FileName=srcfename, FilePath=self.FilesStock + srcfename)

    def DelRecord(self,useremail,paths):
        FindFile = models.UserFileRecord.objects.filter(FilePath__icontains=paths)
        for i in FindFile:
            i.delete()

    def NewName(self,OldPath,NewName):
        pathlist = OldPath.split('/')
        if pathlist[-1] =='':
            del pathlist[-1]
            path = OldPath[0:-1]
        NewPath = OldPath.replace(pathlist[-1],NewName)
        # print(OldPath,NewPath)
        FindFile = models.UserFileRecord.objects.filter(FilePath__icontains=OldPath)
        for i in FindFile:

            i.FilePath = i.FilePath.replace(OldPath,NewPath)
            i.save()



    # students = students.filter(name__icontains=bob)
    # models.UserFileRecord.objects.filter(FilePath__icontains=bob)
