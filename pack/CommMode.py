
import hashlib,os
from SBC import FileType


class ComTol():
    def __init__(self):
        pass

    def size_format(self,size):
        if size < 1024:
            return '%i' % size + 'B'
        elif 1024 <= size < 1024 * 1024:
            return '%.1f' % float(size / 1024) + 'KB'
        elif 1024 * 1024 <= size < 1024 * 1024 * 1024:
            return '%.1f' % float(size / (1024 * 1024)) + 'MB'
        elif 1024 * 1024 * 1024 <= size < 1024 * 1024 * 1024 * 1024:
            return '%.1f' % float(size / (1024 * 1024 * 1024)) + 'GB'
        elif 1024 * 1024 * 1024 * 1024 <= size:
            return '%.1f' % float(size / (1024 * 1024 * 1024 * 1024)) + 'TB'

    def getfileMd5(self,filename):
        if not os.path.isfile(filename):
            return
        myhash = hashlib.md5()
        f = open(filename, "rb")
        while True:
            b = f.read(8096*1024)
            if not b:
                break
            myhash.update(b)
        f.close()
        return myhash.hexdigest()

    def GetImgConPath(self,fepath):
        filtypeOb = FileType.FileType()
        # fetypes = mimetypes.guess_type(fepath)
        # print(fepath,fetypes)
        try:
            fetype = filtypeOb.GetFileType(fepath)
            # fetype = fetypes[0].split('/')[0]
            if fetype[0] == 'image':
                path = '/static/img/filecon/imgcon.jpg'
                return [path, 'img']
                # imgtype = fetype[1]
                # return GetImgconBase64(fepath,imgtype)
            if fetype[0] == 'pdf':
                path = '/static/img/filecon/pdfcon.jpg'
                return [path, 'pdf']
            if fetype[0] == 'word':
                path = '/static/img/filecon/wordcon.jpg'
                return [path, 'word']
            if fetype[0] == 'ppt':
                path = '/static/img/filecon/pptcon.jpg'
                return [path, 'ppt']
            if fetype[0] == 'excel':
                path = '/static/img/filecon/excelcon.jpg'
                return [path, 'excel']
            if fetype[0] == 'zip':
                path = '/static/img/filecon/zipcon.png'
                return [path, 'zip']
            if fetype[0] == 'html':
                path = '/static/img/filecon/htmlcon.jpg'
                return [path, 'html']
            if fetype[0] == 'exe':
                path = '/static/img/filecon/execon.jpg'
                return [path, 'exe']
        except Exception as e:
            print(e)
        return ['/static/img/wj.jfif', 'other']