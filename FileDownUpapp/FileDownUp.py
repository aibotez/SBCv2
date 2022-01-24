from django.http import StreamingHttpResponse,FileResponse
from django.utils.encoding import escape_uri_path
import os

from FileDownUpapp import models




class MakeLink():
    def __init__(self):
        self.FilesStock = r'D:\documents\GitStock\SBCuserTest\FilesStock'

    def mklk(self,dst,srcfename,dstfename):
        # dstDirs = r'D:\documents\GitStock\SBCuserTest\2290227486@qq.com'
        fe = dst+'/'+dstfename
        os.symlink(self.FilesStock+'/'+srcfename,fe)



class FileUp():
    def __init__(self):
        self.FilesInfo=None
        self.FilesStock = 'D:/documents/GitStock/SBCuserTest/FilesStock/'
        self.FileServerHome = 'D:/documents/GitStock/SBCuserTest/'

    def Upfile(self,feMd5,useremail,file_obj):
        if models.FilesStock.objects.filter(FileMd5=feMd5).exists():
            dst =self.FileServerHome+useremail
            dstfename = file_obj.name
            srcfename = models.FilesStock.objects.filter(FileMd5=feMd5).FileName
            lk = MakeLink()
            lk.mklk(dst,srcfename,dstfename)
        else:
            with open(self.FilesStock + file_obj.name, "wb") as f:
                for chunk in file_obj.chunks(chunk_size=2 * 1024 * 1024):
                    f.write(chunk)
            dst =self.FileServerHome+useremail
            dstfename = file_obj.name
            srcfename = file_obj.name
            lk = MakeLink()
            lk.mklk(dst,srcfename,dstfename)

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