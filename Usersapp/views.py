from django.shortcuts import render
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from SBC import FileOper
from django.http import HttpResponse,JsonResponse
from SBC import UserManage
from SBC import LoginVerfiy
# Create your views here.

def GetUserInfo(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return JsonResponse({'error':'login'})
    usermanage = UserManage.usermange()
    try:
        Userinfo = usermanage.GetUserUsedCap(LoginRes['useremail'])
        return JsonResponse(Userinfo)
    except:
        return JsonResponse({'error':1})
