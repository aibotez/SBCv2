import os,shutil
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
        if postdatas['netOper'] == 'MoveFile':
            self.MoveFile(useremail,postdatas)
            return 1
        if postdatas['netOper'] == 'CopyFile':
            self.CopyFile(useremail,postdatas)
            return 1
    def CopyFile(self,useremail,postdatas):
        getuserpath = GetUserPath.GetUserPath()
        move2path = getuserpath.getuserserpath(useremail, postdatas['move2path'])
        movefilesinfo = postdatas['movefilesinfo']
        for i in movefilesinfo:
            movefepath = getuserpath.getuserserpath(useremail,i['fepath'])
            if i['isdir']:
                if os.path.isdir(move2path+i['fename']):
                    shutil.rmtree(move2path + i['fename'])
            else:
                if os.path.exists(move2path+i['fename']):
                    os.remove(move2path + i['fename'])
            try:
                if i['isdir']:
                    shutil.copytree(movefepath,move2path+i['fename'],symlinks=True)
                else:
                    shutil.copyfile(movefepath,move2path+i['fename'],follow_symlinks=False)
            except Exception as e:
                print(e)
        return 1
    def MoveFile(self,useremail,postdatas):
        getuserpath = GetUserPath.GetUserPath()
        move2path = getuserpath.getuserserpath(useremail, postdatas['move2path'])
        movefilesinfo = postdatas['movefilesinfo']
        for i in movefilesinfo:
            movefepath = getuserpath.getuserserpath(useremail,i['fepath'])
            try:
                os.remove(move2path+i['fename'])
            except:
                shutil.rmtree(move2path+i['fename'])
                pass
            try:
                if i['isdir']:
                    shutil.copytree(movefepath,move2path+i['fename'],symlinks=True)
                    shutil.rmtree(movefepath)
                else:
                    shutil.copyfile(movefepath,move2path+i['fename'],follow_symlinks=False)
                    os.remove(movefepath)
            except Exception as e:
                print(e)
        return 1

    def NewFolder(self,useremail,postdatas):
        getuserpath = GetUserPath.GetUserPath()
        userPath = getuserpath.getuserserpath(useremail, postdatas['CurPath'])
        NewFolderName = postdatas['NewFolderName']
        os.makedirs(userPath + NewFolderName)
        return 1