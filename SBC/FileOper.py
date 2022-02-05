import os

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