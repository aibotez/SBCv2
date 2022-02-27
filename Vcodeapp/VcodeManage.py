from pack.SendEmail import SendEmail
from Vcodeapp import models
import time


class VcodeManage():
    def __init__(self):
        self.userdata=None
        self.useremail = None
        self.useripv4 = None

    def saveInfo(self,Vcode):
        # print(self.userdata)
        curtime = int(time.time())
        if self.userdata is None:
            models.Vcodemode.objects.create(useremail=self.useremail, Vcode=Vcode,ipv4=self.useripv4,
                                            ipv6='00.',islocked=0,locklevel=0,firstrequesttime=0,lastrequesttime=curtime,
                                            retimesper=0)
        else:
            self.userdata.Vcode = Vcode
            self.userdata.save()

    def OverForbidTime(self,locklevel,overtime):
        if locklevel < 1:
            return 1
        if locklevel < 2:
            if overtime > 1*60*60/3600:
                return 1
        elif locklevel < 3:
            if overtime > 5*60*60/3600:
                return 1
        elif locklevel < 4:
            if overtime > 12*60*60/3600:
                return 1
        elif locklevel < 5:
            if overtime > 48*60*60/3600:
                return 1
        elif locklevel >= 5:
            return 0
        return 0

    def Updateretimesper(self,userdata,overtime):
        if overtime < 1*60*60:#1*60*60:
            retimesper = userdata.retimesper+1
        else:
            retimesper = 0
        return retimesper
    def Updatelocklevel(self,userdata,overtime):
        locklevel = userdata.locklevel
        if overtime > 2*60*60/3600 and userdata.locklevel < 2:
            locklevel = 0
        elif overtime > 10*60*60/3600 and userdata.locklevel < 3:
            locklevel = 0
        elif overtime > 24*60*60/3600 and userdata.locklevel < 4:
            locklevel = 0
        elif overtime > 100*60*60/3600 and userdata.locklevel < 5:
            locklevel = 0
        return locklevel

    def VerifyVcode(self,useremail,userVcode,dele):
        try:
            userdata = models.Vcodemode.objects.get(useremail=useremail)
            curtime = int(time.time())
            overtime = curtime - userdata.lastrequesttime
            if overtime > 10*60:
                userdata.Vcode = '00'
                userdata.save()
                return 0
            if userdata.Vcode == userVcode and len(userVcode) == 4:
                if int(dele):
                    userdata.Vcode = '01'
                    userdata.save()
                return 1
        except:
            return 0
        return 0

    def VerifyuserRe(self,useremail,useripv4):
        self.useremail = useremail
        self.useripv4 = useripv4
        curtime = int(time.time())
        try:
            self.userdata = models.Vcodemode.objects.get(useremail=useremail)

            if self.userdata.ipv4 != self.useripv4:
                self.userdata.ipv4 = self.useripv4

            overtime = curtime - self.userdata.lastrequesttime
            if self.OverForbidTime(self.userdata.locklevel, overtime):
                self.userdata.islocked = 0
            self.userdata.retimesper = self.Updateretimesper(self.userdata,overtime)
            self.userdata.locklevel = self.Updatelocklevel(self.userdata, overtime)
            self.userdata.lastrequesttime = curtime
            if self.userdata.islocked:
                self.userdata.locklevel = self.userdata.locklevel+1
                return 0
            else:
                if overtime <1:
                    self.userdata.islocked = 1
                    self.userdata.locklevel = self.userdata.locklevel+1
                    # self.userdata.save()
                    return 0
                if self.userdata.retimesper >=5:
                    self.userdata.islocked = 1
                    if self.userdata.locklevel<1:
                        self.userdata.locklevel = 1
                    elif self.userdata.locklevel<2:
                        self.userdata.locklevel = 2
                    elif self.userdata.locklevel<3:
                        self.userdata.locklevel = 3
                    elif self.userdata.locklevel<4:
                        self.userdata.locklevel = 4
                    elif self.userdata.locklevel<5:
                        self.userdata.locklevel = 5
                    # self.userdata.save()
                    return 0
                else:
                    # self.userdata.save()
                    if self.OverForbidTime(self.userdata.locklevel, overtime):
                        self.userdata.islocked = 0
                        return 1
                    else:
                        return 0
        except Exception as e:
            # print(e)
            return 1