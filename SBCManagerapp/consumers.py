import json

from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from SBCManagerapp import models as SBCManagemodels
from SBCManagerapp import Man
from pack import faster_whisper_pack

import time

import numpy as np
import soundfile as sf
import os


def verifylogin(request):
    cookies = request
    LoginRes = {'res': 1, 'useremail': ''}
    if 'coks' in cookies:
        cok = cookies['coks']
        cok = cok.split(';')[-1].replace(' ','')
        usefo = cok.split('auth:')
        if SBCManagemodels.SBCManager.objects.filter(SBCManageEmail=usefo[0]).exists():
            if SBCManagemodels.SBCManager.objects.get(SBCManageEmail=usefo[0]).SBCUserPass0 == usefo[1]:
                LoginRes['res'] = 0
                LoginRes['useremail'] = usefo[0]
                return LoginRes
    return LoginRes

class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.audio_real = faster_whisper_pack.audiomain()

    def vec2wav(self,pcm_vec, wav_file= 'output.wav', framerate=16000):
        """
        将numpy数组转为单通道wav文件
        :param pcm_vec: 输入的numpy向量
        :param wav_file: wav文件名
        :param framerate: 采样率
        :return:
        """
        import wave

        # pcm_vec = np.clip(pcm_vec, -32768, 32768)

        if np.max(np.abs(pcm_vec)) > 1.0:

            pass
            # pcm_vec = pcm_vec/32768.0
            # pcm_vec *= 32767 / max(0.01, np.max(np.abs(pcm_vec)))
        else:
            pcm_vec = pcm_vec * 32768
        # pcm_vec = np.frombuffer(pcm_vec, dtype=np.int16)
        pcm_vec = pcm_vec.astype(np.int16)
        wave_out = wave.open(wav_file, 'wb')
        wave_out.setnchannels(1)
        wave_out.setsampwidth(2)
        wave_out.setframerate(framerate)
        wave_out.writeframes(pcm_vec)



    def save_audio(self,audio_data):


        # 假设你已经有了一个NumPy数组作为音频信号
        # audio_data = np.random.rand(10, 10000)  # 示例数据，实际中这将是你的音频数据
        # 设置音频参数
        sample_rate = 16000  # 示例采样率
        path_to_save = 'output.wav'  # 音频文件保存路径

        # 保存音频数据到文件
        sf.write(path_to_save, audio_data, sample_rate,'PCM_16')
        # sf.write(path_to_save, audio_data, sample_rate)

        print(f'音频文件已保存到: {path_to_save}')

    def websocket_connect(self, message):
        self.accept()

    def websocket_receive(self, message):
        print('connect_in....')
        # print(message)


        info = json.loads(message['text'])
        LoginRes = verifylogin(info)
        if LoginRes['res']:
            print('login+fai')
            self.send(text_data=json.dumps({'res':0}))
        # print(message)
        if 'SerInfos' in info:
            if 'DiskIndex' in info:

                info = Man.Manage().GetSerInfos(1)
            else:
                info = Man.Manage().GetSerInfos()
        elif 'DiskHealthInfo' in info:
            if 'DiskIndex' in info:
                info = Man.Manage().GetDiskInfo(1)
            else:
                info = Man.Manage().GetDiskInfo(0)
        elif 'ModSBCstock' in info:
            ModSBCstock = info['ModSBCstock']
            info = Man.Manage().ModSBCstock(ModSBCstock)
        elif 'GetMountDisks' in info:
            info = {'data':Man.Manage().GetDiskParinfo()}

        elif 'audio_realtime' in info:
            audiodata = info['audiodata']
            # self.save_audio(audiodata)

            # self.vec2wav(np.array(audiodata))

            lagu = info['lagu']
            print('audio_rec')
            if not self.audio_real.model:
                self.audio_real.int()
            self.audio_real.language_chose = lagu
            audiodata = np.array(audiodata,dtype='int16').astype(np.float32) / 32768.0
            # self.save_audio(audiodata)

            # print(audiodata)
            conts = self.audio_real.transcribe_act(audiodata)
            print(conts)
            info = {'data': conts}
            # time.sleep(60)



        info['res'] = 1
        self.send(text_data=json.dumps(info))       # 返回给客户端的消息

    def websocket_disconnect(self, message):
        raise StopConsumer()
