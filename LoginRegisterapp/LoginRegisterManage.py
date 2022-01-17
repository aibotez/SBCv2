from Vcodeapp import models as Vcodemodes
from Usersapp.models import User
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout


class loginOper():
    def __init__(self):
        pass
    def loginact(self):
        pass

class registerOper():
    def __init__(self):
        pass

    def VerifyUser(self,Vcode,useremail,username):
        try:
            userdata = Vcodemodes.Vcodemode.objects.get(useremail=useremail)
            if userdata.Vcode == Vcode:
                if User.objects.filter(username=username).exists() or User.objects.filter(email=useremail).exists():
                    return '用户已存在'
                else:
                    return 1
            else:
                return 'Vcode Error'
        except:
            return 'VcodeVerify Error'

    def registeract(self,userInfos):
        username = userInfos['username']
        userpassword1 = userInfos['userpassword1']
        userpassword2 = userInfos['userpassword2']
        useremail = userInfos['useremail']
        Vcode = userInfos['vcode']
        useripv4 = userInfos['ipv4']

        VerifyUserInfo = self.VerifyUser(Vcode,useremail,username)
        if VerifyUserInfo == 1:
            Cuser = User.objects.create_user(username=username,password=userpassword1,email=useremail,ipv4=useripv4)
            return 1
        return VerifyUserInfo

