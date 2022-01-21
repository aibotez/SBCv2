import urllib.parse
import os,json

class GetUserPath():
    def __init__(self):
        self.ServerHomePath = 'D:/documents/GitStock/SBCuserTest/'

    def GetDownPath(self,DownReInfo,LoginRes):
        DownReInfo = json.loads(DownReInfo)
        useremail = LoginRes['useremail']
        path = DownReInfo['fepath']
        filedownpath = self.ServerHomePath+useremail+path.replace('/home','')
        filedownname = DownReInfo['fename']
        # print(filedownpath,filedownname)
        return {'fename':filedownname,'fepath':filedownpath}

    def userpath(self,req,LoginRes):
        useremail = LoginRes['useremail']
        if 'path' not in req:
            serverpath = self.ServerHomePath+useremail+'/'
            path = '/home/'
            return [path,serverpath]
        path = req['path']
        path = urllib.parse.unquote(path)
        spath = path.replace('/home','')
        serverpath = self.ServerHomePath+useremail+spath
        return [path,serverpath]

    def NewRegisterPath(self,useremail):
        path = self.ServerHomePath+useremail
        try:
            os.makedirs(path)
            return 1
        except:
            return 0

