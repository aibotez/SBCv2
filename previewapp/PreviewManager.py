import os,time,threading,subprocess
from SBC import GetUserPath
import urllib
from urllib import parse
import wave
import cv2





class VideoFram():
    def __init__(self):
        pass

    def get_length(self,filename):
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                 "format=duration", "-of",
                                 "default=noprint_wrappers=1:nokey=1", filename],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        return {'timeduring':float(result.stdout),'fename':os.path.basename(filename)}
    def CreatWav(self,Videopath,Audiopath):
        if os.path.exists(Audiopath):
            os.remove(Audiopath)
        cmd = 'ffmpeg -i {} -f wav {}'.format(Videopath,Audiopath)
        os.system(cmd)


    def GetVideoFrams(self,Videopath,framidexs):
        cap = cv2.VideoCapture(Videopath)
        # cap.set(cv2.CAP_PROP_POS_MSEC, timespan[0])
        cap.set(cv2.CAP_PROP_POS_FRAMES, framidexs[0])  # 设置帧数标记
        frams = []
        curidx = framidexs[0]
        while (cap.isOpened()):
            ret, im = cap.read()  # 获取图像
            if not ret:  # 如果获取失败，则结束
                print("exit")
                break
            frams.append(im.tolist())
            curidx += 1
            if curidx > framidexs[1]:
                break
        return frams

    def GetAudioFrams(self,path,framidexs):
        wf = wave.open(path, 'rb')  # 打开WAV文件
        wf.readframes(framidexs[0])  # 读取第一帧数据
        data = wf.readframes(framidexs[1]-framidexs[0])
        return data
    def GetVideoInfo(self,Videopath,Audiopath):
        # 3 CV_CAP_PROP_FRAME_WIDTH  # 视频帧宽度
        # 4 CV_CAP_PROP_FRAME_HEIGHT  # 视频帧高度
        cap = cv2.VideoCapture(Videopath)
        VideoFramsTotal = cap.get(7)
        VideoFramRate = cap.get(5)
        wf = wave.open(Audiopath, 'rb')  # 打开WAV文件
        AuduoFramsRate = wf.getnframes()
        AudioFramRate = wf.getframerate()
        cap.release()  # 释放视频
        cv2.destroyAllWindows()  # 释放所有显示图像的窗口
        wf.close()
        return {'VideoFramsTotal':VideoFramsTotal,'VideoFramRate':VideoFramRate,'AuduoFramsRate':AuduoFramsRate,'AudioFramRate':AudioFramRate}

class Preview():
    def __init__(self):
        self.VideoFrams = VideoFram()
        self.getuserpath = GetUserPath.GetUserPath()
        self.ConvertState = 0

    def Convert2pdfact(self,useremail,path):
        path = urllib.parse.unquote(path)
        SerPath = self.getuserpath.getuserserpath(useremail, path)
        FileName = os.path.basename(SerPath)
        Convert2Path = 'static/TEMP/{}/{}.pdf'.format(useremail,FileName)
        if not os.path.exists(Convert2Path):
            os.system('unoconv -f pdf -o {} {}'.format(Convert2Path,SerPath))
            # os.system('libreoffice --headless --convert-to pdf {} {}'.format(Convert2Path, SerPath))
            if os.path.exists(Convert2Path):
                return '1'
            else:
                return '0'
        else:
            return '1'


    def Convert2pdf(self,useremail,path):
        try:
            res = self.Convert2pdfact(useremail,path)
            return res
        except:
            return '0'
        # self.ConvertState = 0
        # t = threading.Thread(target=self.Convert2pdfact,args=(useremail,path,))
        # t.setDaemon(True)
        # t.start()
        # while not self.ConvertState:
        #     yield '0'
        # return '1'

    def PrewviewPDF(self,useremail,path):
        SerPath = self.getuserpath.getuserserpath(useremail, path)

    def PreviewVideo(self,useremail,path,req):
        SerPathHome = self.getuserpath.getuserserpath(useremail, '/')
        SerAudFaPath = SerPathHome+'TEMP/'
        VideoFileName = os.path.basename(path)
        AudioFileName = VideoFileName+'.wav'
        if not os.path.isdir(SerAudFaPath):
            os.makedirs(SerAudFaPath)
        AudioPath = SerAudFaPath+AudioFileName
        if not os.path.exists(AudioPath):
            self.VideoFrams.CreatWav(path, AudioPath)
            time.sleep(0.5)
            VideoInfo = self.VideoFrams.GetVideoInfo(path,AudioPath)
            return {'state':'CreatWav','VideoFile':VideoInfo}
        else:
            if 'VideoFram' not in req:
                VideoInfo = self.VideoFrams.GetVideoInfo(path, AudioPath)
                return {'stste':'CreatWavFinish','VideoFile':VideoInfo}
            else:
                VideoFrams = self.VideoFrams.GetVideoFrams(path,req['VideoFram'])
                AudioFrams = self.VideoFrams.GetAudioFrams(AudioPath, req['AudioFram'])
                print(len(VideoFrams),len(AudioFrams))
                # return {'res': 1}
                return {'res': 1, 'AudioFrams':AudioFrams}
