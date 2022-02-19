from django.shortcuts import render
from SBC import LoginVerfiy
from django.http import HttpResponse,JsonResponse
from django.http import HttpResponseRedirect
import json
from SBCShareapp import SBCShareManage
# Create your views here.


def CreatShareFile(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    ShareFileInfo = json.loads(list(request.POST.keys())[0])
    # print(ShareFileInfo)
    req = request.POST.dict()
    SBCShareManages = SBCShareManage.ShareManage()
    res = SBCShareManages.CreatShareUrl(ShareFileInfo,LoginRes,req)
    return HttpResponse(res)