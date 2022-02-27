from Usersapp.models import User

class usermange():
    def __init__(self):
        pass


    def GetUserUsedCap(self,useremail):
       UserInfo = User.objects.get(email=useremail)
       return UserInfo.usedcapacity

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
        UserInfo.save()