import os
from SBC import GetUserPath

class FileOper():
    def __init__(self):
        pass

    def Rename(self,path,NewName):
        pathlist = path.split('/')
        if pathlist[-1] =='':
            del pathlist[-1]
            path = path[0:-1]
        NewPath = path.replace(pathlist[-1],NewName)
        try:
            os.rename(path,NewPath)
            return 1
        except:
            pass
        return 0

class netOper():
    def __init__(self):
        pass

    def netOperMain(self,useremail,postdatas):
        if postdatas['netOper'] == 'NewFilder':
            self.NewFolder(useremail,postdatas)
            return 1

    def NewFolder(self,useremail,postdatas):
        getuserpath = GetUserPath.GetUserPath()
        userPath = getuserpath.getuserserpath(useremail, postdatas['CurPath'])
        NewFolderName = postdatas['NewFolderName']
        os.makedirs(userPath + NewFolderName)
        return 1