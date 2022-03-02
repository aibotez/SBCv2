
import mimetypes


class FileType():
    def __init__(self):
        pass
    def GetFileType(self,fepath):
        fetypes = mimetypes.guess_type(fepath)
        fetype = 'others'
        try:
            Types = fetypes[0].split('/')
            if Types[0] == 'image':
                fetype = 'image'
                return fetype
            if Types[1] == 'pdf':
                fetype = 'pdf'
                return fetype
        except:
            pass
        return fetype