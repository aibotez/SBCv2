
from django.shortcuts import render
from django.shortcuts import redirect
import os,hashlib
from django.contrib.auth.decorators import login_required
from SBC import LoginVerfiy
from django.http import HttpResponse,JsonResponse
from django.http import HttpResponseRedirect
from SBCManagerapp import models as SBCManagemodels
from UserFileRecordapp import models as UserFileRecordmodels
# Create your views here.
from Usersapp.models import User
from SBCManagerapp import Man
from django.contrib.auth import authenticate,login,logout



def size_format(size):
    if size < 1024:
        return '%i' % size + 'B'
    elif 1024 <= size < 1024*1024:
        return '%.1f' % float(size/1024) + 'KB'
    elif 1024*1024 <= size < 1024*1024*1024:
        return '%.1f' % float(size/(1024*1024)) + 'MB'
    elif 1024*1024*1024 <= size < 1024*1024*1024*1024:
        return '%.1f' % float(size/(1024*1024*1024)) + 'GB'
    elif 1024*1024*1024*1024 <= size:
        return '%.1f' % float(size/(1024*1024*1024*1024)) + 'TB'

def LoginVerifyUser(userInfos):
    msg = {'status': 0, 'pass': ''}
    usercount = userInfos['usercount']
    userpassword = userInfos['userpassword']
    # useremail = userInfos['useremail']
    if '@' in usercount:
        UserExist = SBCManagemodels.SBCManager.objects.filter(SBCManageEmail=usercount).exists()

    else:
        UserExist = SBCManagemodels.SBCManager.objects.filter(SBCUser0=usercount).exists()

    if UserExist:
        if '@' in usercount:
            Userfo = SBCManagemodels.SBCManager.objects.get(SBCManageEmail=usercount)
        else:
            Userfo = SBCManagemodels.SBCManager.objects.get(SBCUser0=usercount)
        username = Userfo.SBCUser0
        useremail = Userfo.SBCManageEmail
        if userpassword == Userfo.SBCUserPass0:
            msg['status'] = 1
            msg['pass'] = Userfo.SBCUserPass0
            msg['useremail'] = useremail
            return msg
    return msg
def loginVerify(request):
    if request.method == 'POST':
        request.POST = request.POST.copy()
        userInfos = request.POST.dict()

        res = LoginVerifyUser(userInfos)
        msg = '用户名或密码错误'
        if res['status']:
            response = redirect('/man/')#7 * 24 * 3600
            response.set_cookie('coks', res['useremail'] + 'auth:' + res['pass'])
            # response['coks'] = userInfos['useremail']+'auth:'+res['pass']
            return response
        else:
            return render(request, "SBCManager/sbcmangerlogin.html")
def verifylogin(request):
    cookies = request.COOKIES
    LoginRes = {'res': 1, 'useremail': ''}
    if 'coks' in cookies:
        usefo = cookies['coks'].split('auth:')
        if SBCManagemodels.SBCManager.objects.filter(SBCManageEmail=usefo[0]).exists():
            if SBCManagemodels.SBCManager.objects.get(SBCManageEmail=usefo[0]).SBCUserPass0 == usefo[1]:
                LoginRes['res'] = 0
                LoginRes['useremail'] = usefo[0]
                return LoginRes
    return LoginRes
def GetSerInfo(request):
    info = Man.Manage().GetSerInfo()
    info['Total'] = size_format(info['SBCStockSize'])
    return JsonResponse(info)

def ModCap(request):
    LoginRes = verifylogin(request)
    if LoginRes['res']:
        return render(request, "SBCManager/sbcmangerlogin.html")
    Man.Manage().ModCap(request)
    return HttpResponse('1')
def GetStockFilesAll(request):
    LoginRes = verifylogin(request)
    if LoginRes['res']:
        return render(request, "SBCManager/sbcmangerlogin.html")
    info = Man.Manage().GetFilesAll()
    return JsonResponse(info)
def DelStockFiles(request):
    LoginRes = verifylogin(request)
    if LoginRes['res']:
        return render(request, "SBCManager/sbcmangerlogin.html")
    info = Man.Manage().DelStockFiles(request)
    return JsonResponse(info)
def sbcmanger(request):
    # ManInfo = Man.Manage().GetSerInfo()
    # if not ManInfo:
    #     return
        # SBCManagemodels.SBCManager.objects.create(FileMd5=feMd5, FileName=feMd5+'#'+ srcfename,
        #                                          FilePath=self.FilesStock + feMd5+'#'+ srcfename)
    LoginRes = verifylogin(request)
    if LoginRes['res']:
        return render(request, "SBCManager/sbcmangerlogin.html")
    Users = User.objects.all()
    UserInfo = []
    j = 1
    for i in Users:
        userinfo = {}
        userinfo['username'] = i.username
        userinfo['id'] = i.id
        userinfo['numid'] = str(j)
        userinfo['usedcapacity'] = i.usedcapacity
        userinfo['totalcapacity'] = i.totalcapacity
        userinfo['is_superuser'] = '0'
        if i.is_superuser:
            userinfo['is_superuser'] = '1'
        userinfo['usercapacityper'] = str(round((i.usedcapacity / i.totalcapacity) * 100,1))+'%'
        userinfo['usercapacityinfo'] = '{}/{}  ({})'.format(size_format(i.usedcapacity),size_format(i.totalcapacity),userinfo['usercapacityper'])

        UserInfo.append(userinfo)
        j += 1

    return render(request, "SBCManager/sbcmanager.html", locals())