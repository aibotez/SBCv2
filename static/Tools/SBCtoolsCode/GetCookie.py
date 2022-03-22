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
            'Cookie': self.SBCCookie
        }
        data={
            'usercookie':self.BaiduCookie
        }
        url = 'http://pi.sbc.plus:800/BaiduNetSaveUser/'
        try:
            res = requests.post(url,data=data,headers=headers,timeout=3).text
            res = json.loads(res)
        except:
            return 0
        if res['res'] == '1':
            return 1
        return 0

# 先来个窗口
class window(QWidget):
    cookiess = {}
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
        self.btn_get.clicked.connect(lambda :self.get_cookie('baidu'))  # 绑定按钮点击事件
        self.web = QWebEngineView()  # 创建浏览器组件对象
        self.web.resize(self.ScreeW, self.ScreeH)  # 设置大小
        self.web.load(QUrl(url))  # 打开百度页面来测试
        self.box.addWidget(self.btn_get)  # 将组件放到布局内，先在顶部放一个按钮
        self.box.addWidget(self.web)  # 再放浏览器
        self.web.show()  # 最后让页面显示出来
        QWebEngineProfile.defaultProfile().cookieStore().cookieAdded.connect(self.onCookieAdd)



    def onCookieAdd(self, cookie):  # 处理cookie添加的事件

        domain = cookie.domain()
        name = cookie.name().data().decode('utf-8')  # 先获取cookie的名字，再把编码处理一下
        value = cookie.value().data().decode('utf-8')  # 先获取cookie值，再把编码处理一下
        if domain in self.cookiess:
            _cookie = self.cookiess[domain]
            _cookie[name] = value
        else:
            self.cookiess[domain] = {name:value}  # 将cookie保存到字典里


    # 获取cookie
    def deal_cookie(self,cokuser):
        cookie_str = ''
        for key, value in self.cookiess.items():  # 遍历字典
            if cokuser in key:
                for keyi ,valuei in self.cookiess[key].items():
                    if keyi not in cookie_str:
                        # print(keyi.decode('utf-8') + '=' + valuei.decode('utf-8') + ';')
                        cookie_str += (keyi + '=' + valuei + ';')  # 将键值对拿出来拼接一下
        self.cookiess = {}
        return cookie_str  # 返回拼接好的字符串

    def get_cookie(self,cokuser):
        cookie = self.deal_cookie(cokuser)
        print('获得的Cookie：',cookie)
        # self.btn_get.close()
        # self.btn_get = QPushButton('操作完成，可关闭该窗口！刷新浏览器即可')
        if 'BDUSS' in cookie and 'csrfToken' in cookie and 'pan_login_way' in cookie:
            self.BaiduNetCookie = cookie
            self.btn_get.close()
            self.btn_get = QPushButton('再登录一次小黑云，然后再次点击此按钮')  # 创建一个按钮涌来了点击获取cookie
            self.btn_get.setStyleSheet('''color: black;background-color: pink;''')
            self.btn_get.clicked.connect(lambda :self.get_cookie('sbc'))  # 绑定按钮点击事件
            self.web.close()
            self.web = QWebEngineView()
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
                self.btn_get.setText('操作完成，可关闭该窗口！刷新浏览器即可')
                self.btn_get.disconnect()