from UserFileRecordapp import models
from SBC import FileType

class userfilerecordmanage():
    def __init__(self):
        self.filetype = FileType.FileType()

    def AddNewRecord(self,useremail,path):

        fetype = self.filetype.GetFileType(path)[0]
        if models.UserFileRecord.objects.filter(FilePath = path).exists():
            FindFile = models.UserFileRecord.objects.get(FilePath=path)
            if FindFile.useremail == useremail:
                if FindFile.FileType == fetype:
                    return
                FindFile.FileType = fetype
                FindFile.save()
                return

        models.UserFileRecord.objects.create(useremail = useremail,FileType = fetype,FilePath = path)

    # models.FilesStock.objects.create(FileMd5=feMd5, FileName=srcfename, FilePath=self.FilesStock + srcfename)

    def DelRecord(self,paths):
        FindFile = models.UserFileRecord.objects.filter(FilePath__icontains=paths)

    # students = students.filter(name__icontains=bob)
    # models.UserFileRecord.objects.filter(FilePath__icontains=bob)
