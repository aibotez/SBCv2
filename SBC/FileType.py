
import mimetypes


class FileType():
    def __init__(self):
        pass
    def GetFileType(self,fepath):
        fetypes = mimetypes.guess_type(fepath)
        fetype = 'others'
        try:
            Types = fetypes[0].split('/')
            # print(Types,fepath)
            if Types[0] == 'image':
                fetype = ['image',Types[1]]
                return fetype
            if Types[1] == 'pdf':
                fetype = ['pdf','']
                return fetype
            if 'officedocument.wordprocessingml.document' in Types[1]:
                fetype = ['word','']
                return fetype
            if 'officedocument.presentationml.presentation' in Types[1]:
                fetype = ['ppt','']
                return fetype
        except:
            pass
        return fetype