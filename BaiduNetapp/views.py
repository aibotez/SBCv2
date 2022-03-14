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