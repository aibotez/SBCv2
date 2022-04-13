from UserFileRecordapp import models
from SBC import FileType

class userfilerecordmanage():
    def __init__(self):
        self.filetype = FileType.FileType()

    def AddNewRecord(self,useremail,path):
        fetype = self.filetype.GetFileType(path)
        models.UserFileRecord.objects.create(useremail = useremail,FileType = fetype,FilePath = path)

    # models.FilesStock.objects.create(FileMd5=feMd5, FileName=srcfename, FilePath=self.FilesStock + srcfename)

    def DelRecord(self,paths):
        FindFile = models.UserFileRecord.objects.filter(FilePath__icontains=paths)

    # students = students.filter(name__icontains=bob)
    # models.UserFileRecord.objects.filter(FilePath__icontains=bob)
