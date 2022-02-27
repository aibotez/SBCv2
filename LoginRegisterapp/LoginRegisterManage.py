from Vcodeapp import models as Vcodemodes
from Usersapp.models import User
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from Vcodeapp import VcodeManage
from SBC import GetUserPath

#改密码user.set_password(password)
class loginOper():
    def __init__(self):
        pass

    def LoginVerifyUser(self,userInfos):
        useripv4 = userInfos['ipv4']
        userpassword = userInfos['userpassword']
        useremail = userInfos['useremail']
        msg={'status':0,'pass':''}
        if User.objects.filter(email=useremail).exists():
            Userfo = User.objects.get(email=useremail)
            username = Userfo.username
            if authenticate(username=username,password=userpassword):
                if Userfo.ipv4 == useripv4:
                    pass
                else:
                    Userfo.ipv4 = useripv4
                    Userfo.save()
                msg['status'] = 1
                msg['pass'] = Userfo.password
                return msg
        return msg


class registerOper():
    def __init__(self):
        self.UserIntCap = 100*1024*1024*1024*1024#100GB

    def VerifyUser(self,Vcode,useremail,username):
        try:
            vcodemanage = VcodeManage.VcodeManage()
            VerRes = vcodemanage.VerifyVcode(useremail,Vcode,1)
            # userdata = Vcodemodes.Vcodemode.objects.get(useremail=useremail)
            if VerRes:
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
        msg = {'status':VerifyUserInfo, 'pass': ''}
        if VerifyUserInfo == 1:
            getuserpath = GetUserPath.GetUserPath()
            if getuserpath.NewRegisterPath(useremail):
                print('Register New User')
                Cuser = User.objects.create_user(username=username,password=userpassword1,email=useremail,ipv4=useripv4,usedcapacity = 0,totalcapacity=self.UserIntCap)
                Userfo = User.objects.get(email=useremail)
                msg['status'] = 1
                msg['pass'] = Userfo.password
                return msg
            msg['status'] = '用户文件创建失败'
            return msg
        return msg

