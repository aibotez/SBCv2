import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

import MainShowWindow
import GetCookie
import Bai1
import time

import os,hashlib


def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename ,"rb")
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()
def size_format(size):
    if size < 1024:
        return '%i' % size + 'size'
    elif 1024 <= size < 1024*1024:
        return '%.1f' % float(size/1024) + 'KB'
    elif 1024*1024 <= size < 1024*1024*1024:
        return '%.1f' % float(size/(1024*1024)) + 'MB'
    elif 1024*1024*1024 <= size < 1024*1024*1024*1024:
        return '%.1f' % float(size/(1024*1024*1024)) + 'GB'
    elif 1024*1024*1024*1024 <= size:
        return '%.1f' % float(size/(1024*1024*1024*1024)) + 'TB'
class Speedcount():
    def __init__(self):
        self.time0 = time.time()
        self.FileCurSize = 0
    def GetSpeed(self,CurSize):
        time2 = time.time()
        speed = size_format((CurSize-self.FileCurSize)/(time2-self.time0))
        self.time0 = time2
        self.FileCurSize = CurSize
        return speed


def UpdateProgress(ut,BD,speedCur):
    ut.label_4.setText('{}/{}'.format(size_format(BD.CurDownSize), size_format(BD.FileInfo['FileSize'])))
    speed = speedCur.GetSpeed(BD.CurDownSize)
    ut.label_5.setText(speed + '/s')
    progressvaule = int((BD.CurDownSize / BD.FileInfo['FileSize']) * 100)
    ut.progressBar.setValue(progressvaule)
    print(BD.CurDownSize,BD.FileInfo['FileSize'],BD.DownStation)
    if BD.CurDownSize >= BD.FileInfo['FileSize'] and BD.DownStation==1:
        ut.progressBar.setProperty("value", 100)
        DownFileMd5 = GetFileMd5(BD.FileInfo['FileName'])
        FileActMd5 = BD.FileInfo['FileMd5']
        if FileActMd5 == BD.FileInfo['FileName']:
            FileActMd5 = DownFileMd5
        if DownFileMd5 == FileActMd5:
            ut.label_5.setText('下载完成！')
        else:
            ut.label_5.setText('文件校验错误！')
        ut.timer.stop()


def Down(ut):
    speedCur = Speedcount()
    url = ut.textEdit.toPlainText()
    BD = Bai1.Bd(url)
    ut.label_4.setText('0/{}'.format(size_format(BD.FileInfo['FileSize'])))
    ut.label_3.setText(BD.FileInfo['FileName'])
    t1 = time.time()
    ut.timer.timeout.connect(lambda :UpdateProgress(ut,BD,speedCur))
    ut.timer.start(700)
    BD.ThreadAct()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    Main = QMainWindow()
    ui = MainShowWindow.Ui_SBC_Tool()
    ui.setupUi(Main)
    subuiGetcok = GetCookie.window()
    ui.pushButton.clicked.connect(lambda :subuiGetcok.show())
    ui.pushButton_2.clicked.connect(lambda :Down(ui))
    Main.show()
    sys.exit(app.exec_())