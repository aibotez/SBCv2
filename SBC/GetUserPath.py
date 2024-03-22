import urllib.parse
import os,json
from SBCManagerapp import Man



#Serinfo = Man.Manage().InitSerPath()
#FileUsersPath = Serinfo['user']
#FileStockPath = Serinfo['stock']
class GetUserPath():
    def __init__(self):
        # self.ServerHomePath = 'D:/documents/GitStock/SBCuserTest/'
        # self.ServerHomePath = '/mnt/SBC/SBCUsers/'
        self.Serinfo = Man.Manage().InitSerPath()
        
        self.ServerHomePath = self.Serinfo['user']

    def GetDownPath(self,DownReInfo,LoginRes):

        DownReInfo = urllib.parse.unquote(DownReInfo)
        DownReInfo = json.loads(DownReInfo)
        useremail = LoginRes['useremail']
        path = DownReInfo['fepath']
        filedownpath = self.ServerHomePath+useremail+path.replace('/home','')
        filedownname = DownReInfo['fename']
        # print(filedownpath,filedownname)
        DownReInfo['fepath'] = filedownpath
        return DownReInfo
        # return {'fename':filedownname,'fepath':filedownpath}

    def getuserserpath(self,useremail,userpath):
        spath = userpath.replace('/home', '')
        serverpath = self.ServerHomePath + useremail + spath
        return serverpath

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

