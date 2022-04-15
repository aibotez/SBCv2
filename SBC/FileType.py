
import mimetypes
import filetype

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
            if Types[0] == 'video':
                fetype = ['video',Types[1]]
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
            if 'officedocument.spreadsheetml.sheet' in Types[1]:
                fetype = ['excel','']
                return fetype
            if 'compressed' in Types[1] or 'tar' in Types[1]:
                fetype = ['zip','']
                return fetype
            if 'html' in Types[1]:
                fetype = ['html','']
                return fetype
            if 'x-msdownload' in Types[1]:
                fetype = ['exe','']
                return fetype
        except:
            pass

        try:
            kind = filetype.guess(fepath)
            if 'compressed' in kind.mime:
                fetype = ['zip','']
                return fetype
        except:
            pass
        return fetype