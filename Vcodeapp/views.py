from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from pack.SendEmail import SendEmail
from Vcodeapp import models



Em = SendEmail.EmailManage()
# Create your views here.
def GetVcode(request):
    Vcode = Em.GenerateVCode()

    return HttpResponse('5684')

def VerifyVcode(request):
    print(request.GET)
    Vcode = request.GET['Vcode']
    if Vcode == '1234':
        return HttpResponse('1')
    return HttpResponse('0')

def Vcodedb_handle(Useremail,VCode,Ipv4,Ipv6):

    models.Vcodemode.objects.create(useremail=Useremail,password='123456',age=33)
    return HttpResponse('OK')