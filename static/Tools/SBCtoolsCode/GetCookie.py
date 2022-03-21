import sys,requests,json
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton



class SendCookie():
    def __init__(self,BaiduCookie,SBCCookie):
        self.BaiduCookie = BaiduCookie
        self.SBCCookie = SBCCookie
    def SendCookieact(self):
        headers = {
            'Cookie': 'coks = {}'.format(self.SBCCookie)
        }

        data={
            'usercookie':self.BaiduCookie
        }
        url = 'http://pi.sbc.plus:800/BaiduNetSaveUser'
        res = requests.post(url,data=data,headers=headers).text
        res = json.loads(res)
        if res['res'] == '1':
            return 1


# 先来个窗口
class window(QWidget):#QWidget
    def __init__(self):
        super().__init__()
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.BaiduNetCookie=''
        self.SBCCookie = ''
        self.ScreeW = self.screenRect.width()
        self.ScreeH = self.screenRect.height()
        self.setup("https://pan.baidu.com/")


    def setup(self,url):
        self.box = QVBoxLayout(self)  # 创建一个垂直布局来放控件
        self.btn_get = QPushButton('完成登录后，点击此按钮获取cookies')  # 创建一个按钮涌来了点击获取cookie
        self.btn_get.setStyleSheet('''color: black;background-color: pink;''')
        self.btn_get.clicked.connect(self.get_cookie)  # 绑定按钮点击事件
        self.web = MyWebEngineView()  # 创建浏览器组件对象
        self.web.resize(self.ScreeW, self.ScreeH)  # 设置大小
        self.web.load(QUrl(url))  # 打开百度页面来测试
        self.box.addWidget(self.btn_get)  # 将组件放到布局内，先在顶部放一个按钮
        self.box.addWidget(self.web)  # 再放浏览器
        self.web.show()  # 最后让页面显示出来


    def get_cookie(self):
        cookie = self.web.get_cookie()
        print('获取到cookie: ', cookie)
        # self.btn_get.close()
        # self.btn_get = QPushButton('操作完成，可关闭该窗口！刷新浏览器即可')
        if 'BDUSS' in cookie:
            self.BaiduNetCookie = cookie
            self.btn_get.close()
            self.btn_get = QPushButton('再登录一次小黑云，然后再次点击此按钮')  # 创建一个按钮涌来了点击获取cookie
            self.btn_get.setStyleSheet('''color: black;background-color: pink;''')
            self.btn_get.clicked.connect(self.get_cookie)  # 绑定按钮点击事件
            self.web.close()
            self.web = MyWebEngineView()
            self.web.resize(self.ScreeW, self.ScreeH)
            self.web.load(QUrl("http://pi.sbc.plus:800/"))
            self.box.addWidget(self.btn_get)  # 将组件放到布局内，先在顶部放一个按钮
            self.box.addWidget(self.web)  # 再放浏览器
            self.web.show()
        if 'coks' in cookie:
            self.SBCCookie = cookie
        if self.BaiduNetCookie !='' and self.SBCCookie != '':
            sendCok = SendCookie(self.BaiduNetCookie,self.SBCCookie)
            if sendCok.SendCookieact():
                self.btn_get.close()
                self.btn_get = QPushButton('操作完成，可关闭该窗口！刷新浏览器即可')



# 创建自己的浏览器控件，继承自QWebEngineView
class MyWebEngineView(QWebEngineView):
    def __init__(self, *args, **kwargs):
        super(MyWebEngineView, self).__init__(*args, **kwargs)
        # 绑定cookie被添加的信号槽
        QWebEngineProfile.defaultProfile().cookieStore().cookieAdded.connect(self.onCookieAdd)
        self.cookies = {}  # 存放cookie字典

    def onCookieAdd(self, cookie):  # 处理cookie添加的事件
        name = cookie.name().data().decode('utf-8')  # 先获取cookie的名字，再把编码处理一下
        value = cookie.value().data().decode('utf-8')  # 先获取cookie值，再把编码处理一下
        self.cookies[name] = value  # 将cookie保存到字典里

    # 获取cookie
    def get_cookie(self):
        cookie_str = ''
        for key, value in self.cookies.items():  # 遍历字典
            cookie_str += (key + '=' + value + ';')  # 将键值对拿出来拼接一下
        return cookie_str  # 返回拼接好的字符串

# import tkinter



# if __name__ == "__main__":
#     # from tkinter import *
#     # from tkinterie.tkinterIE import WebView
#     # a = Tk()
#     # a.geometry('700x500+100+100')
#     # w = WebView(a, 500, 500, 'www.baidu.com')
#     # w.pack(expand=True, fill='both')
#     #
#     # a.mainloop()
#
#
#     app = QApplication(sys.argv)
#     w = window()
#     w.show()
#     sys.exit(app.exec_())

