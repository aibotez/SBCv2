import requests,os,time
import threading,hashlib



class Bd():
    def __init__(self,url):
        self.url = url
        self.headers = {}
        self.ThreadDownAccept = 0
        self.FileMD5 = '0'
        self.headinit()
        self.FileInfo = {}
        self.GetFileInfo()
        # self.FileInitOffset = 0
        # self.GetCureSize()
        self.ThreadNums = 4
        self.FileChunks = []
        # self.SplitFile()

        self.timeStart = time.time()

        self.CurDownSize = 0

        self.TLock=threading.Lock()

        self.DownStation = 0



    def GetFileMd5(self,filename):
        if not os.path.isfile(filename):
            return
        myhash = hashlib.md5()
        f = open(filename, "rb")
        while True:
            b = f.read(8096)
            if not b:
                break
            myhash.update(b)
        f.close()
        return myhash.hexdigest()

    def headinit(self):
        self.headers = {
            'User-Agent': 'netdisk;P2SP;3.0.0.127',
            'Connection': 'Keep - Alive',
            'accept-language':'zh-CN,zh;q=0.9',
            # 'Host': 'bdcm01.baidupcs.com',
            # 'Range': 'bytes=0-102400'
        }

    def GetFileName(self,response):
        req = response.headers

        # print(req)
        if 'Content-Disposition' in req:
            fename = req['Content-Disposition']
            if 'name=' in fename:
                name = fename.split('name=')[-1]
                name = name.replace("'",'')
                name = name.replace('"', '').encode('ISO-8859-1').decode('utf-8')
                return name

            name = req['Content-Disposition'].split('"')[-2].encode('ISO-8859-1').decode('utf-8')
            return name
        if response.url != self.url:
            from urllib.parse import urlsplit
            name = os.path.basename(urlsplit(response.url)[2])
            return name
        else:
            return os.path.basename(self.url)
    def GetSize(self,response):
        header = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        }
        req = response.headers
        if 'Content-Range' in req:
            FileSize = int(req['Content-Range'].split('/')[-1])
            self.ThreadDownAccept = 1
            return FileSize
        response1 = requests.get(self.url, headers=header,stream=True)
        req = response1.headers
        FileSize = int(req['Content-Length'])
        self.ThreadDownAccept = 0
        return FileSize
    def GetFileMd5byNet(self,response):
        import base64
        req = response.headers
        for i in req.keys():
            if 'md5' in i.lower():
                FileMd5Base64 = base64.b64encode(req[i].encode("utf-8")).decode('utf-8')
                self.FileMD5 = FileMd5Base64


    def GetFileInfo(self):
        self.headers['Range'] = 'bytes=0-0'
        response = requests.get(self.url, headers=self.headers,stream=True)
        # req = response.headers
        name = self.GetFileName(response)
        # print(name)
        FileSize = self.GetSize(response)
        self.GetFileMd5byNet(response)
        if self.FileMD5 == '0':
            self.FileMD5 = name
        # name = req['Content-Disposition'].split('"')[-2].encode('ISO-8859-1').decode('utf-8')
        # FileSize = int(req['Content-Range'].split('/')[-1])
        # FileMd5 = req['Content-MD5']
        self.FileInfo = {'FileName':name,'FileSize':FileSize,'FileMd5':self.FileMD5}
        print(self.FileInfo)
    def SplitFile(self):
        if self.ThreadDownAccept == 0:
            self.ThreadNums = 1

        FileSizeTotal = self.FileInfo['FileSize']
        self.FileChunks = []
        for i in range(self.ThreadNums):
            idx1 = i*int(FileSizeTotal/self.ThreadNums)+0
            if i == self.ThreadNums-1:
                idx2 = FileSizeTotal-1+1
            else:
                idx2 = idx1+int(FileSizeTotal/self.ThreadNums)-1
            fes = [idx1,idx2]
            chunkName = self.FileInfo['FileMd5']+'#'+str(idx1)+'-'+str(idx2)
            self.FileChunks.append({'FileChunk':fes,'ChunkName':chunkName,'StartPosition':0})

    def CheckFileChunk(self):
        FileMd5 = self.FileInfo['FileMd5']
        CurPath = os.getcwd()
        files = []

        LocalDownFileChunks = []
        for root, dirs, filess in os.walk(CurPath):
            for i in filess:
                if FileMd5 in i:
                    chunk = i.split('#')[-1]
                    LocalDownFileChunks.append(int(chunk.split('-')[-1]))
                    files.append({'ChunkName':i,'Chunk':chunk})
            break
        if len(files) == 0:
            return 0
        self.FileChunks = []
        for i in files:
            DownSize = os.path.getsize(i['ChunkName'])
            self.CurDownSize = self.CurDownSize + DownSize
            FileChunk_Start = int(i['Chunk'].split('-')[0])
            FileChunk_End = int(i['Chunk'].split('-')[1])

            FileChunkStart = FileChunk_Start+DownSize
            if FileChunkStart >= FileChunk_End:
                FileChunkStart = FileChunk_End
                FileChunkEnd = FileChunkStart

            else:
                FileChunkEnd = FileChunk_End
            self.FileChunks.append({'FileChunk': [FileChunkStart,FileChunkEnd], 'ChunkName':i['ChunkName'],'StartPosition':DownSize})
        LocalDownFileMaxChunk = max(LocalDownFileChunks)
        if LocalDownFileMaxChunk < self.FileInfo['FileSize']:
            ChunkName = self.FileInfo['FileMd5']+'#{}-{}'.format(LocalDownFileMaxChunk,self.FileInfo['FileSize'])
            self.FileChunks.append({'FileChunk': [LocalDownFileMaxChunk,self.FileInfo['FileSize']], 'ChunkName':ChunkName,'StartPosition':0})
        self.ThreadNums = len(self.FileChunks)

        return 1




    def ThreadAct(self):
        if self.ThreadDownAccept==0:
            t = threading.Thread(target=self.Dow1,args=(0,))
            t.setDaemon(True)
            t.start()
            return 1
        checkFechunk = self.CheckFileChunk()
        if not checkFechunk:
            self.SplitFile()
        # self.fd = open(self.FileInfo['FileName'], "wb")
        t_list = []
        # info = self.FileChunks[0]
        # t1 = threading.Thread(target=self.Dow1, args=(info,))
        # t1.setDaemon(True)
        # t1.start()
        for i in range(self.ThreadNums):
            info = self.FileChunks[i]
            globals()[self.FileChunks[i]['ChunkName']] = threading.Thread(target=self.Dow1,args=(info,))
            globals()[self.FileChunks[i]['ChunkName']].setDaemon(True)
            globals()[self.FileChunks[i]['ChunkName']].start()
            # globals()[self.FileChunks[i]['ChunkName']].join()
            t_list.append(globals()[self.FileChunks[i]['ChunkName']])
        # for i in range(self.ThreadNums):
        #     t_list[i].join()

    def MergeFileChunk(self):
        print('DownFinish-MergeFile')
        with open(self.FileInfo['FileName'],'wb') as fm:

            FileList = {}
            NumList = []
            for i in self.FileChunks:
                fechunkend = i['FileChunk'][-1]
                FileList[str(fechunkend)] = {'ChunkName':i['ChunkName']}
                NumList.append(fechunkend)
            NumList = sorted(NumList)

            for j in NumList:
                i = FileList[str(j)]
                # print(i['ChunkName'])
                with open(i['ChunkName'],'rb') as f:
                    while True:
                        fechunk = f.read(100*1024*1024)
                        if fechunk:
                            # print('chunkSize:',len(fechunk))
                            fm.write(fechunk)
                        else:
                            break
                try:
                    # pass
                    os.remove(i['ChunkName'])
                except Exception as e:
                    print(e)
        self.DownStation = 1
        print('MergeFinish')

    def GetCureSize(self,FileName):
        return os.path.getsize(FileName)

    def StreamDown(self):
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        }
        # if os.path.exists(self.FileInfo['FileName']):
        #     os.remove(self.FileInfo['FileName'])
        with open(self.FileInfo['FileName'], "wb") as fchunk:
            with requests.get(self.url, headers=headers, stream=True) as req:
                for chunk in req.iter_content(chunk_size=512*1024):
                    if chunk:
                        self.CurDownSize = self.CurDownSize + len(chunk)
                        fchunk.write(chunk)
                    else:
                        self.DownStation = 1
                        break

    def OtherDown(self,FeInfo):
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
            'Connection': 'Keep - Alive',
            # 'Host': 'bdcm01.baidupcs.com',
            # 'Range': 'bytes=0-102400'
        }
        startpos = FeInfo['FileChunk'][0]
        endpos = FeInfo['FileChunk'][1]
        coutsize = endpos - startpos
        feoffset = startpos
        headers['Range'] = 'bytes={}-{}'.format(str(feoffset), str(endpos))
        if not os.path.exists(FeInfo['ChunkName']):
            with open(FeInfo['ChunkName'], "wb") as feC:
                feC.write(b'')
        feoffset = 0
        with open(FeInfo['ChunkName'], "r+b") as fchunk:
            # fchunk.seek(FeInfo['StartPosition'])
            with requests.get(self.url, headers=headers, stream=True) as req:
                for chunk in req.iter_content(chunk_size=512*1024):
                    if chunk:
                        self.TLock.acquire()
                        self.CurDownSize = self.CurDownSize + len(chunk)
                        self.TLock.release()
                        fchunk.seek(FeInfo['StartPosition']+feoffset)
                        fchunk.write(chunk)
                        feoffset = feoffset + len(chunk)
                    else:
                        self.DownStation = 1
                        break
        if self.CurDownSize >= self.FileInfo['FileSize']:
            self.MergeFileChunk()

    def Dow1(self,FeInfo):

        if self.ThreadDownAccept == 0:
            self.StreamDown()
            self.DownStation = 1
            return 1
        if 'baidu' not in self.url and 'dp-logid' not in self.url:
            self.OtherDown(FeInfo)
            return 1
        headers = {
            'User-Agent': 'netdisk;P2SP;3.0.0.127',
            'Connection': 'Keep - Alive',
            # 'Host': 'bdcm01.baidupcs.com',
            # 'Range': 'bytes=0-102400'
        }

        startpos = FeInfo['FileChunk'][0]
        endpos = FeInfo['FileChunk'][1]
        lenL = 1024 * 400
        # lenL = 1024 * 10
        coutsize = endpos - startpos
        rangNum = int(coutsize/lenL)+1
        se = 0
        t1 = time.time()
        feoffset = startpos
        if not os.path.exists(FeInfo['ChunkName']):
            with open(FeInfo['ChunkName'], "wb") as feC:
                feC.write(b'')

        with open(FeInfo['ChunkName'], "r+b") as fchunk:
            while True:
                feidxend = feoffset + lenL
                if feidxend > endpos:
                    feidxend = endpos
                headers['Range'] = 'bytes={}-{}'.format(str(feoffset), str(feidxend))
                req = requests.get(self.url, headers=headers)
                if len(req.content) == int(req.headers['Content-Length']):
                    fchunk.seek(feoffset-startpos+FeInfo['StartPosition'])
                    fchunk.write(req.content)
                feoffset = feoffset + lenL + 1
                se += len(req.content)
                self.TLock.acquire()
                self.CurDownSize = self.CurDownSize + len(req.content)
                self.TLock.release()
                if feoffset > endpos:
                    break
        if self.CurDownSize >= self.FileInfo['FileSize']:
            self.MergeFileChunk()


# url = 'https://cdn4.mydown.com/623affc5/5e34431239485546c1977ab08a1d9f22/newsoft/3__5000557__3f7372633d6c6d266c733d6e32393464323930613961__68616f2e3336302e636e__0c6b.exe'
# url = 'https://download.jetbrains.com/python/pycharm-community-2021.3.3.exe?_gl=1*1du2fct*_ga*MjEyMjQ2OTkyNS4xNjM2MjA4NTI0*_ga_V0XZL7QHEB*MTY0ODAyNjIzNi41LjAuMTY0ODAyNjIzNi4w&_ga=2.8012918.572347722.1648016234-2122469925.1636208524'
# # # url = 'https://allall01.baidupcs.com/file/cf8a08925421b695e8303093076db8bf?bkt=en-26dcfdb4e5ee1a499dee4ab6e168c91309a1886b96512db5554252c6dac76c07b31a08073a7f21e0&fid=2820270452-250528-53268081162635&time=1648014784&sign=FDTAXUbGERLQlBHSKfWaqi-DCb740ccc5511e5e8fedcff06b081203-4D5RWnRsPWPicG%2FdGXjCP7hmHtg%3D&to=79&size=1115475552&sta_dx=1115475552&sta_cs=467&sta_ft=esd&sta_ct=7&sta_mt=7&fm2=MH%2CXian%2CAnywhere%2C%2C%E4%B8%8A%E6%B5%B7%2Cany&ctime=1517297834&mtime=1578908100&resv0=-1&resv1=0&resv2=rlim&resv3=2&resv4=1115475552&vuk=2820270452&iv=0&htype=&randtype=&tkbind_id=0&esl=1&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-444aa45ed77f292be8d490755f52141393089a94be5cec322787aa64c0badfdaef91ece364e6f556&sl=78053454&expires=8h&rt=pr&r=150501622&vbdid=4173101684&fin=SXC_2018LTSB_X64.esd&bflag=79,18-79&err_ver=1.0&check_blue=1&rtype=1&clienttype=9&channel=0&dp-logid=8809565293028790037&dp-callid=0.1&hps=1&tsl=120&csl=120&fsl=-1&csign=1I1eQUvOcDQFvOtRoQe6TT6LH2o%3D&so=0&ut=6&uter=0&serv=0&uc=2314189907&ti=970a8ec65273ef12230065b9576767b1d9ccdf649a1df586&sta_eck=1&hflag=30&from_type=0&adg=c_6c3e20d8811253d6c5007b12f0561376&reqlabel=250528_l_0d379c25691f1db02fd2dff786ffd19a_-1_b47a1c84a207d217ae9410ea0984f09f&ibp=1&by=themis'
#
# url = 'https://xacu01.baidupcs.com/file/1ef41338d1208a58e8019f78476b9133?bkt=en-e031c0692dcd5a21460dfcce047dacdff039c647c0068ce08212eba07fed317911992bea2539482b&fid=2820270452-250528-322862895774618&time=1648126443&sign=FDTAXUbGERLQlBHSKfWqi-DCb740ccc5511e5e8fedcff06b081203-hGEcOJi2iKfRHyuCiHfw3EWZ%2BOc%3D&to=128&size=11585609&sta_dx=11585609&sta_cs=0&sta_ft=zip&sta_ct=7&sta_mt=7&fm2=MH%2CXian%2CAnywhere%2C%2Canhui%2Ccnc&ctime=1539081506&mtime=1539081506&resv0=-1&resv1=0&resv2=rlim&resv3=2&resv4=11585609&vuk=2820270452&iv=0&htype=&randtype=&tkbind_id=0&esl=1&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-a6e0c16c99979b797080dc4278489322bc08a96fc2d4b72364d9f279dacf95c4275f83daf8a95e7d&sl=78053454&expires=8h&rt=pr&r=937514969&vbdid=-&fin=CAJViewer7%E5%85%8D%E5%AE%89%E8%A3%85.zip&bflag=128,79,303,18-128&err_ver=1.0&check_blue=1&rtype=1&clienttype=9&channel=0&dp-logid=8839538435313853808&dp-callid=0.1&hps=1&tsl=120&csl=120&fsl=-1&csign=1I1eQUvOcDQFvOtRoQe6TT6LH2o%3D&so=0&ut=6&uter=0&serv=0&uc=2314189907&ti=e292035734ac599541a1b88b4a84623b694eb9582f70f386c48031c257b32a4e&sta_eck=1&hflag=30&from_type=0&adg=c_195dcffd0ac4803330e489f48a738c43&reqlabel=250528_l_b79ee2ecbae2d617456e21c155258c29_-1_e25c92e6da30f5e414c0ac16cefb99e1&ibp=1&by=themis'
# BD = Bd(url)
# # BD.ThreadAct()
# # #
# # while True:
# #     print(BD.CurDownSize)
# #     time.sleep(0.5)
# #     if BD.DownStation == 1:
# #         break

