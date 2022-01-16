from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse,FileResponse
from urllib import parse
import shutil,json,io
import socket,os,time,threading
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from PIL import Image

# from pack.SendEmail import SendEmail
# from Vcodeapp import models
#
#
# Em = SendEmail.EmailManage()
# Vcode = Em.GenerateVCode()
# Em.SendMessagebyQq('2290227486@qq.com',Vcode,'163')

def Home(request):
    return render(request, "login/login.html")

# def login(request):
#     return render(request, "login/login.html")
#
# def Register(request):
#     return render(request, "register/register_v2.html")

# def GetVcode(request):
#     Vcode = Em.GenerateVCode()
#
#     return HttpResponse('5684')
#
# def VerifyVcode(request):
#     print(request.GET)
#     Vcode = request.GET['Vcode']
#     if Vcode == '1234':
#         return HttpResponse('1')
#     return HttpResponse('0')

@require_POST
def registerVerify(request):
    if request.method == 'POST':
        userInfos = request.POST
        username = userInfos['username']
        userpassword = userInfos['userpassword1']
        useremail = userInfos['useremail']
        vcode = userInfos['vcode']
        return HttpResponse('ok')

# import time
# t1 = int(time.time())
# print(t1,type(t1))
# time.sleep(2)
# t2 = int(time.time())
# print(t2)
# print(t2-t1)

