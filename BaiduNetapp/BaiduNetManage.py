from BaiduNetapp.models import BaiduNetUserManage
import time,requests,json,base64
from urllib.parse import quote,unquote


class baidunet():
    def __init__(self,cookie):
        self.cookies = cookie
        self.headers = ''
        self.PulublicHearders()

        self.ShareId =''
        self.ShareUk = ''
        self.FsId = ''
        self.timestamp = ''
        self.bdclnd = ''
    def PulublicHearders(self):
        self.headers = {
            # 'User-Agent' : 'netdisk;4.6.2.0;PC;PC-Windows;10.0.10240;WindowsBaiduYunGuanJia',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
            'Cookie':self.cookies,
            'Host': 'pan.baidu.com',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'navigate',
            'Referer': 'https://pan.baidu.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
    def size_format(self,size):
        size = int(size)
        if size < 1024:
            return '%i' % size + 'size'
        elif 1024 <= size < 1024 * 1024:
            return '%.1f' % float(size / 1024) + 'KB'
        elif 1024 * 1024 <= size < 1024 * 1024 * 1024:
            return '%.1f' % float(size / (1024 * 1024)) + 'MB'
        elif 1024 * 1024 * 1024 <= size < 1024 * 1024 * 1024 * 1024:
            return '%.1f' % float(size / (1024 * 1024 * 1024)) + 'GB'
        elif 1024 * 1024 * 1024 * 1024 <= size:
            return '%.1f' % float(size / (1024 * 1024 * 1024 * 1024)) + 'TB'

    def FormTime(self,times):
        format = '%Y-%m-%d %H:%M'
        time_tuple = time.localtime(times)
        result = time.strftime(format, time_tuple)
        return result

    def GetFileType(self,fe):
        if fe['isdir'] == 1:
            return 'folder'
        fename = fe['server_filename']
        fetype = fename.split('.')

        if len(fetype) < 1:
            return 'other'
        fetype = fetype[-1].lower()
        imgtypre = ['bmp','jpg','png','tif','gif''pcx','tga','exif','fpx','svg','psd','cdr','pcd','dxf','ufo','eps','ai','raw','WMF','webp','avif','apng']
        if fetype in imgtypre:
            return 'img'
        if fetype == 'pdf':
            return 'pdf'
        if fetype == 'exe':

            return 'exe'
        if 'doc' in fetype:
            return 'word'
        if 'ppt' in fetype:
            return 'ppt'
        if 'xls' in fetype:
            return 'excel'
        if 'html' in fetype:
            return 'html'
        if fetype in ['7z','zip','rar']:
            return 'zip'
        return 'other'

    def GetConImg(self,fe):
        fetype = self.GetFileType(fe)
        if fetype == 'folder':
            return '/static/img/foldersm.png'
        if fetype == 'img':
            path = '/static/img/filecon/imgcon.jpg'
            return path
            # imgtype = fetype[1]
            # return GetImgconBase64(fepath,imgtype)
        if fetype == 'pdf':
            path = '/static/img/filecon/pdfcon.jpg'
            return path
        if fetype == 'word':
            path = '/static/img/filecon/wordcon.jpg'
            return path
        if fetype == 'ppt':
            path = '/static/img/filecon/pptcon.jpg'
            return path
        if fetype == 'exe':
            path = '/static/img/filecon/execon.jpg'
            return path
        if fetype == 'excel':
            path = '/static/img/filecon/excelcon.jpg'
            return path
        if fetype == 'zip':
            path = '/static/img/filecon/zipcon.png'
            return path
        if fetype == 'html':
            path = '/static/img/filecon/htmlcon.jpg'
            return path
        else:
            return '/static/img/wj.jfif'

    def GetFileList(self,path):
        urlSer = 'https://pan.baidu.com/api/list?&dir={}'.format(quote(path))
        headers = {
            'Cookie':self.cookies
        }
        res = requests.get(urlSer,headers=headers).text
        resdata = json.loads(res)
        if resdata['errno'] ==0:
            for i in range(len(resdata['list'])):
                filepath = base64.encodebytes(resdata['list'][i]['path'].encode('utf8')).decode()
                filepath = filepath.replace('\n', '')
                resdata['list'][i]['filelj'] = filepath
                resdata['list'][i]['imgpath'] = self.GetConImg(resdata['list'][i])
                resdata['list'][i]['size'] = self.size_format(resdata['list'][i]['size'])
                resdata['list'][i]['server_mtime'] = self.FormTime(resdata['list'][i]['server_mtime'])
        return resdata

class manage():
    def __init__(self):
        pass

    def CheckBaiduNetUserExist(self,LoginRes):
        userEmail = LoginRes['useremail']
        if BaiduNetUserManage.objects.filter(useremail=userEmail).exists():
            BaiduNetUserData = BaiduNetUserManage.objects.get(useremail=userEmail)
            if len(BaiduNetUserData.cookie)<10:
                return {'errno':'404'}
            return {'errno':'0','cookie':BaiduNetUserData.cookie}
        return {'errno': '404'}
    def baidunetShow(self,LoginRes,showpath):
        checkre = self.CheckBaiduNetUserExist(LoginRes)
        if checkre['errno'] == 404:
            return checkre
        bdnOp = baidunet(checkre['cookie'])
        bdndatas = bdnOp.GetFileList(showpath)
        return bdndatas
    def BaiduNetSaveUser(self,LoginRes,usercookie):
        userEmail = LoginRes['useremail']
        BaiduNetUserManage.objects.create(useremail=userEmail,cookie=usercookie)
        return 1
