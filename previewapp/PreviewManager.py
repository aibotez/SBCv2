import os,time
from SBC import GetUserPath
import urllib
from urllib import parse

class Preview():
    def __init__(self):
        self.getuserpath = GetUserPath.GetUserPath()

    def Convert2pdf(self,useremail,path):
        print(path)
        path = urllib.parse.unquote(path)
        print(path)
        SerPath = self.getuserpath.getuserserpath(useremail, path)
        FileName = os.path.basename(SerPath)
        Convert2Path = 'static/TEMP/{}/{}.pdf'.format(useremail,FileName)
        os.system('unoconv -f pdf -o {} {}'.format(Convert2Path,SerPath))
        return '1'

    def PrewviewPDF(self,useremail,path):
        SerPath = self.getuserpath.getuserserpath(useremail, path)