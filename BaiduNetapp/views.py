from django.shortcuts import render
from SBC import LoginVerfiy
from django.http import HttpResponse,JsonResponse
from django.http import HttpResponseRedirect
import json
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from BaiduNetapp import BaiduNetManage
# Create your views here.

@require_POST
def BaiduNetUserExistCheck(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    manage = BaiduNetManage.manage()
    bdn = manage.CheckBaiduNetUserExist(LoginRes)
    return JsonResponse(bdn)
@require_POST
def BaiduNetShow(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    manage = BaiduNetManage.manage()
    bdn = manage.baidunetShow(LoginRes)

@require_POST
def BaiduNetSaveUser(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    manage = BaiduNetManage.manage()
    manage.BaiduNetSaveUser(LoginRes,request.POST.get('usercookie'))
    return JsonResponse({'res':'1'})