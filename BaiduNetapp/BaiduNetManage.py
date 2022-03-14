from BaiduNetapp.models import BaiduNetUserManage
import time,requests,json
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
    def GetFileList(self,path):
        urlSer = 'https://pan.baidu.com/api/list?&dir={}'.format(quote(path))
        headers = {
            'Cookie':self.cookies
        }
        res = requests.get(urlSer,headers=headers).text
        resdata = json.loads(res)
        # for i in resdata['list']:
        #     if i['isdir']=='0':
        #         print(i['server_filename'], i['path'], i['fs_id'], i['isdir'], self.size_format(i['size']),
        #               self.FormTime(i['server_mtime']),i['md5'])
        #     else:
        #         print(i['server_filename'], i['path'], i['fs_id'], i['isdir'], self.size_format(i['size']),
        #               self.FormTime(i['server_mtime']))
        return resdata

class manage():
    def __init__(self):
        pass

    def CheckBaiduNetUserExist(self,LoginRes):
        userEmail = LoginRes['useremail']
        if BaiduNetUserManage.objects.filter(useremail=userEmail).exists():
            BaiduNetUserData = BaiduNetUserManage.objects.get(useremail=userEmail)
            if len(BaiduNetUserData.cookie<10):
                return 0
            return BaiduNetUserData.cookie
    def baidunetShow(self,LoginRes):
        checkre = self.CheckBaiduNetUserExist(LoginRes)
        if checkre == 0:
            return '0'
        bdnOp = baidunet(checkre)
        bdndatas = bdnOp.GetFileList('/')
        return bdndatas
