from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from pack.SendEmail import SendEmail
from Vcodeapp import models
import time
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from Vcodeapp import VcodeManage


Em = SendEmail.EmailManage()


# Create your views here.
def GetVcode(request):
    useremail = request.GET['useremail']
    userinfo = request.META
    if 'HTTP_X_FORWARDED_FOR' in userinfo.keys():
        useripv4 = request.META['HTTP_X_FORWARDED_FOR']
    else:
        useripv4 = request.META['REMOTE_ADDR']
    # print(useripv4)
    Vcode =''
    msg='0'
    vcodemanage=VcodeManage.VcodeManage()
    if vcodemanage.VerifyuserRe(useremail,useripv4):
        Vcode = Em.GenerateVCode()
        Em.SendVcodeby(useremail,Vcode,'163')
        # Vcode = 'test'
        msg='1'
    vcodemanage.saveInfo(Vcode)
    return HttpResponse(msg)

def VerifyVcode(request):
    vcodemanage = VcodeManage.VcodeManage()
    Vcode = request.GET['Vcode']
    useremail = request.GET['email']
    if vcodemanage.VerifyVcode(useremail,Vcode,0):
        return HttpResponse('1')
    return HttpResponse('0')


