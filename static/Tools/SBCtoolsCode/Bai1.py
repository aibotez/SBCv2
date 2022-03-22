import requests,os,time
import threading,hashlib



class Bd():
    def __init__(self,url):
        self.url = url
        self.headers = {}
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
            # 'Host': 'bdcm01.baidupcs.com',
            # 'Range': 'bytes=0-102400'
        }

    def GetFileInfo(self):
        self.headers['Range'] = 'bytes=0-0'
        req = requests.get(self.url, headers=self.headers).headers
        # print(req)
        name = req['Content-Disposition'].split('"')[-2]
        FileSize = int(req['Content-Range'].split('/')[-1])
        FileMd5 = req['Content-MD5']
        self.FileInfo = {'FileName':name,'FileSize':FileSize,'FileMd5':FileMd5}
        print(self.FileInfo)
    def SplitFile(self):
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
        for root, dirs, filess in os.walk(CurPath):
            for i in files:
                if FileMd5 in i:
                    chunk = i.split('#')[-1]
                    files.append({'ChunkName':i,'Chunk':chunk})
            break
        if len(files) == 0:
            return 0
        self.FileChunks = []
        for i in files:
            DownSize = os.path.getsize(i['ChunkName'])
            FileChunk_Start = int(i['Chunk'].split('-')[0])
            FileChunk_End = int(i['Chunk'].split('-')[1])

            FileChunkStart = FileChunk_Start+DownSize
            if FileChunkStart >= FileChunk_End:
                FileChunkEnd = FileChunkStart
            else:
                FileChunkEnd = FileChunk_End
            self.FileChunks.append({'FileChunk': [FileChunkStart,FileChunkEnd], 'ChunkName':i['ChunkName'],'StartPosition':DownSize})
        self.ThreadNums = len(self.FileChunks)
        return 1




    def ThreadAct(self):
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
            for i in self.FileChunks:
                print(i['ChunkName'])
                with open(i['ChunkName'],'rb') as f:
                    while True:
                        fechunk = f.read(100*1024*1024)
                        if fechunk:
                            print('chunkSize:',len(fechunk))
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

    def Dow1(self,FeInfo):
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
        with open(FeInfo['ChunkName'], "wb") as fchunk:
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


url = 'https://allall01.baidupcs.com/file/7480f8fbcb3dacc3ed3eb7f033346de0?bkt=en-3f603aaf96443402be6e916f43c68ba0d374eb70134fd229f017b01668b633d2a3c6e778914680f7d15c1d0ad5857c064002858af055864e9e56fb9cd4e184ef&fid=2820270452-250528-764152255893183&time=1647956728&sign=FDTAXUbGERLQlBHSKfWqi-DCb740ccc5511e5e8fedcff06b081203-EiJr8bCZBDXb1jMpE3ozIJxZlyU%3D&to=79&size=4146432&sta_dx=4146432&sta_cs=0&sta_ft=zip&sta_ct=7&sta_mt=7&fm2=MH%2CYangquan%2CAnywhere%2C%2C%E4%B8%8A%E6%B5%B7%2Cany&ctime=1516323582&mtime=1535854715&resv0=-1&resv1=0&resv2=rlim&resv3=2&resv4=4146432&vuk=2820270452&iv=0&htype=&randtype=&tkbind_id=0&esl=1&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-092769b8cb66bc6f26fb790597085168228d76697ca9ac1e6990e4250ba28ea011f1d93eec2eb80632636c30f81aeab7478f7d111c8ad10b305a5e1275657320&sl=78053454&expires=8h&rt=pr&r=411873133&vbdid=4173101684&fin=EFI--10.13.zip&bflag=79,18-79&err_ver=1.0&check_blue=1&rtype=1&clienttype=9&channel=0&dp-logid=8793980870229136870&dp-callid=0.1&hps=1&tsl=120&csl=120&fsl=-1&csign=1I1eQUvOcDQFvOtRoQe6TT6LH2o%3D&so=0&ut=6&uter=0&serv=0&uc=2314189907&ti=e5c35a8e2eeea51069cf30d9e408ab1170f75ba6da1efd55&sta_eck=1&hflag=30&from_type=0&adg=c_6c3e20d8811253d6c5007b12f0561376&reqlabel=250528_l_0d379c25691f1db02fd2dff786ffd19a_-1_b47a1c84a207d217ae9410ea0984f09f&ibp=1&by=themis'
BD = Bd(url)
BD.ThreadAct()

while True:
    print(BD.CurDownSize)
    time.sleep(0.5)
    if BD.DownStation == 1:
        break

