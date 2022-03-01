
import mimetypes


class FileType():
    def __init__(self):
        pass
    def GetFileType(self,fepath):
        fetypes = mimetypes.guess_type(fepath)
        fetype = 'others'
        try:
            fetype = fetypes[0].split('/')[0]
        except:
            pass
        return fetype