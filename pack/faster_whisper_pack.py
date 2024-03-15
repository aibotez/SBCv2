from faster_whisper import WhisperModel

import numpy as np

class audiomain():

    def __init__(self):
        # self.p = pyaudio.PyAudio()
        # self.during = 2
        # self.RATE = 16000
        # self.CHUNK = int(self.RATE/10)
        # self.stream = None
        self.language_chose = 'en'
        self.model_path = 'faster_whisper_model/small/'
        self.model = None
        # self.aud_datas = {}
        # self.aud_max_list=[]


    def int(self):
        self.model = WhisperModel(model_size_or_path=self.model_path, local_files_only=True, device='cpu',
                                  compute_type="int8")

    def transcribe_act(self,aud_data):
        # global aud_datas
        print('start.')
        segments, info = self.model.transcribe(aud_data, language=self.language_chose, vad_filter=True,
                                               vad_parameters=dict(min_silence_duration_ms=1000))
        for segment in segments:
            print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))


    # def findInternalRecordingDevice(self):
    #     # 要找查的设备名称中的关键字
    #     target = '立体声混音'
    #     # 逐一查找声音设备
    #     for i in range(self.p.get_device_count()):
    #         devInfo = self.p.get_device_info_by_index(i)
    #         if devInfo['name'].find(target) >= 0 and devInfo['hostApi'] == 0:
    #             print('已找到内录设备,序号是 ', i)
    #             return i
    #     print('无法找到内录设备!')

    # def create_audio_stream(self,selected_device_index):
    #     RATE = self.RATE
    #     FORMAT = pyaudio.paInt16
    #     CHANNELS = 1
    #     # audio = pyaudio.PyAudio()
    #     stream = self.p.open(
    #         format=FORMAT,
    #         channels=CHANNELS,
    #         rate=RATE,
    #         input=True,
    #         input_device_index=selected_device_index,
    #         frames_per_buffer=self.CHUNK,
    #         # stream_callback=callback,
    #     )
    #     return stream
    #
    # def aud_record(self):
    #     # global aud_datas
    #
    #     # np.concatenate(self.speech_buffer)
    #     # silence_threshold = 500
    #     i = 1
    #     while True:
    #         aud_fams = []
    #         self.aud_max_list = []
    #
    #         aud_data0 = self.stream.read(self.CHUNK, exception_on_overflow=False)
    #         aud_data0 = np.frombuffer(aud_data0, dtype=np.int16)
    #         energy = np.max(aud_data0)
    #         aud_fram_clip_s=0
    #         while aud_fram_clip_s<int(self.during*self.RATE/self.CHUNK) or energy >= np.mean(self.aud_max_list)/2.7:
    #             self.aud_max_list.append(energy)
    #             aud_data = aud_data0.astype(np.float32) / 32768.0
    #             aud_fams.append(aud_data)
    #             aud_data0 = self.stream.read(self.CHUNK, exception_on_overflow=False)
    #             aud_data0 = np.frombuffer(aud_data0, dtype=np.int16)
    #             energy = np.max(aud_data0)
    #
    #             aud_fram_clip_s += 1
    #
    #
    #         aud_data = np.concatenate(aud_fams)
    #         self.aud_datas[i] = aud_data
    #         i+=1








    # def main(self):
    #     idx = int(self.findInternalRecordingDevice())
    #     self.stream = self.create_audio_stream(idx)
    #     self.model = WhisperModel(model_size_or_path=self.model_path, local_files_only=True, device='cpu', compute_type="int8")
    #
    #     # pro_aud_record = Process(target=self.aud_record, name='aud_record')
    #     # pro_aud_record.start()
    #
    #
    #     th_aud_record = threading.Thread(target=self.aud_record)
    #     th_aud_record.setDaemon(True)
    #     th_aud_record.start()
    #
    #     # th_transcribe_act = threading.Thread(target=self.transcribe_act)
    #     # th_transcribe_act.setDaemon(True)
    #     # th_transcribe_act.start()
    #     #
    #     # while True:
    #     #     pass