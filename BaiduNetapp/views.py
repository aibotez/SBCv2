from django.shortcuts import render
from SBC import LoginVerfiy
from django.http import HttpResponse,JsonResponse
from django.http import HttpResponseRedirect
import json
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from BaiduNetapp import BaiduNetManage
from urllib.parse import quote,unquote
# Create your views here.

@require_POST
def BaiduNetUserExistCheck(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    manage = BaiduNetManage.manage()
    bdn = manage.CheckBaiduNetUserExist(LoginRes)
    return JsonResponse(bdn)
# @require_POST
import base64
def GetNavpath(path):
    navpath = 'home'+path
    navpathlist = navpath.split('/')
    navpaths = []
    s = ''
    for i in navpathlist:
        s = s+i+'/'
        s = s.replace('home','')
        Npath = base64.encodebytes(s.encode('utf8')).decode()
        Npath = Npath.replace('\n', '')
        navpaths.append({'navname':i,'path':s,'pathId':Npath})
    return navpaths


def BaiduNetHome(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    showpath = '/'
    if request.method == 'GET':
        showpath = request.GET['showpath']
    else:
        showpath = request.POST['showpath']
    showpath = unquote(showpath)
    manage = BaiduNetManage.manage()
    BaiduNetUserInfo = manage.GetBaiduNetUserInfo(LoginRes)
    return render(request,'BaiduNet/BaiduNetHome.html',locals())


def BaiduNetShow(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')

    showpath = '/'
    if request.method == 'GET':
        showpath = request.GET['showpath']
    else:
        showpath = request.POST['showpath']
    showpath = unquote(showpath)
    manage = BaiduNetManage.manage()
    bdn = manage.baidunetShow(LoginRes,showpath)
    data = bdn['list']
    navlist = GetNavpath(showpath)
    navlastpath = navlist[-1]['path']
    return render(request, "BaiduNet/BaiduNetFileList.html", locals())

@require_POST
def BaiduNetSaveUser(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    manage = BaiduNetManage.manage()
    manage.BaiduNetSaveUser(LoginRes,request.POST.get('usercookie'))
    return JsonResponse({'res':'1'})

@require_POST
def GetBDDownLink(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    data = request.POST
    # print(data,data['fepath'])
    manage = BaiduNetManage.manage()
    DownLink = manage.GetBaiduNetDownLinkFromPan(data['fepath'],LoginRes)

    return JsonResponse({'errno':'0','DownLink':DownLink})

from django.shortcuts import redirect
def reD(request):

    url = request.GET['url']
    burldata = base64.b64decode(url).decode("utf-8")
    # print(burldata)
    response = redirect(burldata)
    heardes = {
        'User-Agent': 'netdisk;P2SP;3.0.0.127',
        # 'Cookie':'BDUSS=WlEMzN1T25sRTgybnFaflJkUjVuOEc2VUZNc2c3TGtiLWVhME0zQ3Z6Qk12c0ZoSVFBQUFBJCQAAAAAAAAAAAEAAACnqKsdZGxvZWNxaTQyMjM0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEwxmmFMMZphW;STOKEN=c5816c3b29a51273a34621968b5b96fe55b8dca9381014d2ce64789e28419409;STOKEN=c5816c3b29a51273a34621968b5b96fe55b8dca9381014d2ce64789e28419409',
        # 'Connection': 'Keep - Alive',
        # 'Host': 'bdcm01.baidupcs.com',
        'Range': 'bytes=0-1024'
    }
    response.headers = heardes
    print(response.headers)
    return response