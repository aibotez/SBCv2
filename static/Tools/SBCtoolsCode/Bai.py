import requests,os,time
import threading,hashlib



class Bd():
    def __init__(self,url):
        self.url = url
        self.headers = {}
        self.headinit()
        self.FileInfo = {}
        self.GetFileInfo()
        self.FileInitOffset = 0
        self.GetCureSize()
        self.ThreadNums = 4
        self.FileChunks = []
        self.SplitFile()

        self.timeStart = time.time()

        self.CurDownSize = 0

        self.TLock=threading.Lock()

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
            self.FileChunks.append({'FileChunk':fes,'ChunkName':chunkName})

        # print(self.FileChunks)
    def ThreadAct(self):
        self.fd = open(self.FileInfo['FileName'], "wb")
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
                    fm.write(f.read())
                    # while True:
                    #     fechunk = f.read(100*1024*1024)
                    #     if fechunk:
                    #         fm.write(fechunk)
                    #     else:
                    #         break
                try:
                    pass
                    # os.remove(i['ChunkName'])
                except Exception as e:
                    print(e)
        print('MergeFinish')

    def GetCureSize(self):
        FileSize = 0
        if os.path.exists(self.FileInfo['FileName']):
            FileSize = os.path.getsize(self.FileInfo['FileName'])
        self.FileInitOffset = FileSize

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
        j = 0

        while True:
            j = j + 1

            if self.CurDownSize >= self.FileInfo['FileSize']:
                break
            feidxend = feoffset + lenL
            if feidxend > endpos:
                feidxend = endpos
            headers['Range'] = 'bytes={}-{}'.format(str(feoffset), str(feidxend))
            req = requests.get(self.url, headers=headers)
            # print('Judge',len(req.content),req.headers['Content-Length'],feoffset,feidxend-feoffset+1)
            # self.TLock.acquire()
            if len(req.content) == int(req.headers['Content-Length']):
                self.fd.seek(feoffset)
                self.fd.write(req.content)
            # self.TLock.release()
            feoffset = feoffset + lenL + 1
            se += len(req.content)
            # print(se / 1024,se / 1024 / (time.time() - t1))
            self.TLock.acquire()
            self.CurDownSize = self.CurDownSize + len(req.content)
            self.TLock.release()
            # print(self.CurDownSize, self.FileInfo['FileSize'])
            if feoffset > endpos:
                break



    def Dow(self,chunk_size=64*1024):
        se = 0
        t1 = time.time()
        url = 'https://allall01.baidupcs.com/file/9a7addeeb65712ca0184a4951342e961?bkt=en-e031c0692dcd5a21fac4346467693d3ab753b71627885f59947514293a00645d33168c14cbd1e87f&fid=2820270452-250528-725418911330523&time=1647748795&sign=FDTAXUbGERLQlBHSKfWaqi-DCb740ccc5511e5e8fedcff06b081203-n08uUe1sPBLQKnHetLmJD0zBf3I%3D&to=79&size=2001982065&sta_dx=2001982065&sta_cs=2411&sta_ft=zip&sta_ct=7&sta_mt=7&fm2=MH%2CQingdao%2CAnywhere%2C%2C%E4%B8%8A%E6%B5%B7%2Cany&ctime=1553091296&mtime=1563893307&resv0=-1&resv1=0&resv2=rlim&resv3=2&resv4=2001982065&vuk=2820270452&iv=0&htype=&randtype=&tkbind_id=0&esl=1&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-2962428ada002d2a545f0abbf6659e23734c08732a630cd45d21068779d172cd7224453c1e8f0f20&sl=78053454&expires=8h&rt=pr&r=816458019&vbdid=4173101684&fin=Illustrator+CC2019.zip&bflag=79,18-79&err_ver=1.0&check_blue=1&rtype=1&clienttype=9&channel=0&dp-logid=8738164438237176022&dp-callid=0.1&hps=1&tsl=120&csl=120&fsl=-1&csign=1I1eQUvOcDQFvOtRoQe6TT6LH2o%3D&so=0&ut=6&uter=0&serv=0&uc=2314189907&ti=3dbf888e013f6563a90e3f0e036fc0be4ec74e8d54af6319&sta_eck=1&hflag=30&from_type=0&adg=c_6c3e20d8811253d6c5007b12f0561376&reqlabel=250528_l_0d379c25691f1db02fd2dff786ffd19a_-1_b47a1c84a207d217ae9410ea0984f09f&ibp=1&by=themis'

        self.headers['Range'] = 'bytes={}-{}'.format(str(0), str(1024))



        with requests.get(url,headers=self.headers,stream=True) as req:
            for chunk in req.iter_content(chunk_size=chunk_size):
                if chunk:
                    print(len(chunk))
                    # yield chunk
                else:
                    print(chunk)
                    break




# if __name__ == '__main__':
#     url = 'https://allall01.baidupcs.com/file/6773ef5f8l935228e8d2b6fbd9d6a1f9?bkt=en-24c643f198a62f88e1b7f5a1e399ae48049a882d557991bd73e660cdabaebee71b78d532dbe679a1&fid=2820270452-250528-162810124701119&time=1647838624&sign=FDTAXUbGERLQlBHSKfWqi-DCb740ccc5511e5e8fedcff06b081203-Bjqm%2Fq4VO8w8rzpIBtRJJEqx8ws%3D&to=79&size=12638494&sta_dx=12638494&sta_cs=0&sta_ft=zip&sta_ct=6&sta_mt=6&fm2=MH%2CXian%2CAnywhere%2C%2C%E4%B8%8A%E6%B5%B7%2Cany&ctime=1626267845&mtime=1626267845&resv0=-1&resv1=0&resv2=rlim&resv3=2&resv4=12638494&vuk=2820270452&iv=0&htype=&randtype=&tkbind_id=0&esl=1&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-84e8033c7bcda1a16a05d172b7a18a2b7ba814a2514e598175209d33da89a4a0b54966c680689ee9&sl=78053454&expires=8h&rt=pr&r=302150972&vbdid=4173101684&fin=personal_file%281%29.zip&bflag=79,18-79&err_ver=1.0&check_blue=1&rtype=1&clienttype=9&channel=0&dp-logid=8762277623307746971&dp-callid=0.1&hps=1&tsl=120&csl=120&fsl=-1&csign=1I1eQUvOcDQFvOtRoQe6TT6LH2o%3D&so=0&ut=6&uter=0&serv=0&uc=2314189907&ti=497b2742088ef3a39df9f4618ed7c010fae1a18e46701649&sta_eck=1&hflag=30&from_type=1&adg=c_6c3e20d8811253d6c5007b12f0561376&reqlabel=250528_l_0d379c25691f1db02fd2dff786ffd19a_-1_b47a1c84a207d217ae9410ea0984f09f&ibp=1&by=themis'
#
#     t1 = time.time()
#     te = Bd(url)
#     te.ThreadAct()
#
#     while True:
#         t2 = time.time()
#         speed = te.CurDownSize/(t2-t1)
#         print(speed/1024,str(te.CurDownSize)+'/'+str(te.FileInfo['FileSize']))
#         if te.CurDownSize >= te.FileInfo['FileSize']:
#             break



