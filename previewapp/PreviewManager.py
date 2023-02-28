import os,time,threading,subprocess
from SBC import GetUserPath
import urllib
from urllib import parse
import wave
import numpy as np
import cv2,base64
from django.http import HttpResponse,JsonResponse





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
        image_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 视频帧宽度
        image_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 视频帧高度
        image_channel = 3  # RGB 3通道
        # cap.set(cv2.CAP_PROP_POS_MSEC, timespan[0])
        cap.set(cv2.CAP_PROP_POS_FRAMES, framidexs[0])  # 设置帧数标记
        frams = []
        curidx = framidexs[0]
        cursize = 0
        # img_batch_rgb = np.empty(shape=[0, image_height, image_width, image_channel], dtype=np.uint8)
        for i in range(framidexs[0],framidexs[1]+1):
            # print(i)
            ret, im = cap.read()  # 获取图像
            if not ret:  # 如果获取失败，则结束
                print("exit")
                break
            # opencv:BGR  转换为 RGB
            # rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # im = base64.b64encode(im).decode()
            # img_batch_rgb = np.append(img_batch_rgb, np.expand_dims(im, 0), axis=0)
            frams.append(im.tobytes())
            # yield im
        # print(len(frams))
        # img_batch_rgb = base64.b64encode(img_batch_rgb).decode()
        return frams
        # while (cap.isOpened()):
        #     ret, im = cap.read()  # 获取图像
        #     if not ret:  # 如果获取失败，则结束
        #         print("exit")
        #         break
        #     frams.append(im)
        #     # frams.append(base64.b64encode(im).decode())
        #     curidx += 1
        #     # cursize += len(base64.b64encode(im).decode())
        #     if curidx > framidexs[1]:
        #         # print('cursize',cursize/1024/1024)
        #         break
        # return frams

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

def TimeFormat(t0):
    hour = int(t0/60/60)
    if hour < 0:
        hourstr = '00'
    else:
        if hour <10:
            hourstr = '0'+str(int(hour))
        else:
            hourstr = str(int(hour))
    tm0 = t0 - int(hour)*60*60
    tm = tm0/60
    if tm < 0:
        minstr = '00'
    else:
        if tm <10:
            minstr = '0'+str(int(tm))
        else:
            minstr = str(int(tm))
    ts = tm0 - int(tm) * 60
    if ts < 10:
        Secstr = '0'+str(int(ts))
    else:
        Secstr = str(int(ts))

    return hourstr+':'+minstr+':'+Secstr
class ClipVideo():
    def __init__(self):
        pass
    def get_length(self,filename):
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                 "format=duration", "-of",
                                 "default=noprint_wrappers=1:nokey=1", filename],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        print(filename)
        return {'timeduring':float(result.stdout),'fename':os.path.basename(filename)}
    def cutVideo(self,path, TEMPpath,timespan):
        videoName = '{}/{}_{}#'.format(TEMPpath, timespan[0], timespan[1]) + os.path.basename(path)
        if os.path.exists(videoName):
            os.remove(videoName)
        # 'ffmpeg -i input.mp4 -ss 00:01:20 -t 02:00:00 -vcodec copy -acodec copy output.mp4'
        command = 'ffmpeg -ss {} -i {} -to {} -vcodec copy -flags +global_header -acodec copy  {}'.format(TimeFormat(timespan[0]),path,
                                                                                    TimeFormat(timespan[1]), videoName)
        os.system(command)
        videocount = None
        try:
            with open(videoName,'rb') as f:
                videocount = f.read()
            os.remove(videoName)
        except:
            pass
        return videocount


class Preview():
    def __init__(self):
        self.VideoFrams = VideoFram()
        self.ClipVideo = ClipVideo()
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
        SerAudFaPath = SerPathHome+'TEMP/video'
        VideoFileName = os.path.basename(path)
        AudioFileName = VideoFileName+'.wav'
        if not os.path.isdir(SerAudFaPath):
            os.makedirs(SerAudFaPath)

        if 'VideoFram' not in req:
            VideoInfo = self.ClipVideo.get_length(path)
            return JsonResponse(VideoInfo)
        else:
            VideoFrams = self.ClipVideo.cutVideo(path, SerAudFaPath,req['VideoFram'])
            return HttpResponse(VideoFrams, content_type='application/octet-stream')
        #
        # AudioPath = SerAudFaPath+AudioFileName
        # if not os.path.exists(AudioPath):
        #     self.VideoFrams.CreatWav(path, AudioPath)
        #     time.sleep(0.5)
        #     VideoInfo = self.VideoFrams.GetVideoInfo(path,AudioPath)
        #     return {'state':'CreatWav','VideoFile':VideoInfo}
        # else:
        #     if 'VideoFram' not in req and 'AudioFram' not in req:
        #         VideoInfo = self.VideoFrams.GetVideoInfo(path, AudioPath)
        #         return JsonResponse({'stste':'CreatWavFinish','VideoFile':VideoInfo})
        #         # return {'stste':'CreatWavFinish','VideoFile':VideoInfo}
        #     elif 'VideoFram' in req:
        #         # t1 = time.time()
        #         VideoFrams = self.VideoFrams.GetVideoFrams(path,req['VideoFram'])
        #         AudioFrams = self.VideoFrams.GetAudioFrams(AudioPath, req['AudioFram'])
        #         # t2 = time.time()
        #         # AudioFrams = self.VideoFrams.GetAudioFrams(AudioPath, req['AudioFram'])
        #         # t3 = time.time()
        #         # print(t3-t1,t2-t1)
        #         # print(len(VideoFrams),len(AudioFrams))
        #         # # return {'res': 1}
        #         # res = {'res': 1, 'VideoFrams': VideoFrams, 'AudioFrams': AudioFrams}
        #         return JsonResponse({'VideoFrams':base64.b64encode(VideoFrams).decode(),'AudioFrams':base64.b64encode(AudioFrams).decode()})
        #         # return HttpResponse(VideoFrams, content_type='application/octet-stream')
        #         # return {'res': 1, 'VideoFrams': VideoFrams, 'AudioFrams': AudioFrams}
        #         # return {'res': 1, 'VideoFrams':VideoFrams,'AudioFrams':base64.b64encode(AudioFrams).decode()}
        #     elif 'AudioFram' in req:
        #         AudioFrams = self.VideoFrams.GetAudioFrams(AudioPath, req['AudioFram'])
        #         return HttpResponse(AudioFrams, content_type='application/octet-stream')
