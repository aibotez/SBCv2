import os,time,threading
from SBC import GetUserPath
import urllib
from urllib import parse

class Preview():
    def __init__(self):
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