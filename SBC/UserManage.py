from Usersapp.models import User

class usermange():
    def __init__(self):
        pass

    def size_format(self,size):
        if size < 1024:
            return '%i' % size + 'size'
        elif 1024 <= size < 1024 * 1024:
            return '%.1f' % float(size / 1024) + 'KB'
        elif 1024 * 1024 <= size < 1024 * 1024 * 1024:
            return '%.1f' % float(size / (1024 * 1024)) + 'MB'
        elif 1024 * 1024 * 1024 <= size < 1024 * 1024 * 1024 * 1024:
            return '%.1f' % float(size / (1024 * 1024 * 1024)) + 'GB'
        elif 1024 * 1024 * 1024 * 1024 <= size:
            return '%.1f' % float(size / (1024 * 1024 * 1024 * 1024)) + 'TB'

    def GetUserUsedCap(self,useremail):
       UserInfo = User.objects.get(email=useremail)
       usedCap = UserInfo.usedcapacity
       totalCap = UserInfo.totalcapacity
       usedcappercent = usedCap/totalCap
       usedcappercentstr = self.size_format(usedCap)+'/'+self.size_format(totalCap)
       return {'usedpercent':usedcappercent,'usedcappercentstr':usedcappercentstr,'username':UserInfo.username}

    def Capisfull(self,useremail,NewFeSize):
        UserInfo = User.objects.get(email=useremail)
        if UserInfo.usedcapacity + NewFeSize > UserInfo.totalcapacity:
            return 1
        return 0

    def AddUsedCap(self,useremail,NewFesize):
        UserInfo = User.objects.get(email=useremail)
        UserInfo.usedcapacity = UserInfo.usedcapacity + NewFesize
        UserInfo.save()

    def DelUsedCap(self,useremail,NewFesize):
        UserInfo = User.objects.get(email=useremail)
        UserInfo.usedcapacity = UserInfo.usedcapacity - NewFesize
        if UserInfo.usedcapacity <0:
            UserInfo.usedcapacity = 0
        UserInfo.save()