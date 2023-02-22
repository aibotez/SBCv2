from django.shortcuts import render
from SBC import LoginVerfiy
from django.http import HttpResponse,JsonResponse
from django.http import HttpResponseRedirect
import json
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from SBCShareapp import SBCShareManage
# Create your views here.


@require_POST
def CreatShareFile(request):

    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    try:
        ShareFileInfo = json.loads(list(request.POST.keys())[0])
    except:
        ShareFileInfo = json.loads(request.body)
    # print(ShareFileInfo)
    req = request.POST.dict()
    reqHeadres = request.headers
    # if 'Host'

    CurUrl = reqHeadres['Host']
    SBCShareManages = SBCShareManage.ShareManage()
    res = SBCShareManages.CreatShareUrl(ShareFileInfo,LoginRes,CurUrl)
    return JsonResponse({'res':res})
    # return HttpResponse()
def GetShareFile(request):
    ShareLink = request.GET['SBCShare']


def ShareSave2SBC(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')

    ShareFileInfo = json.loads(request.body)
    SBCShareManages = SBCShareManage.ShareManage()
    # print(ShareFileInfo)
    res = SBCShareManages.Save2SBC(ShareFileInfo,LoginRes)
    return JsonResponse({'res': res})

def GetSBCShareFile(request):
    data = request.GET
    ShareLink = data['ShareLink']
    Password = data['PassWord']
    Path = data['path']
    SBCShareManages = SBCShareManage.ShareManage()
    res = SBCShareManages.GetShareInfo(ShareLink,Password,Path)
    return JsonResponse({'res': res})

def SBCShareShow(request):
    data = request.GET
    SBCShareManages = SBCShareManage.ShareManage()
    ShareLink = request.GET['SBCShare']

    res = SBCShareManages.ShareCheck(ShareLink)
    if res !='pass':
        return JsonResponse({'check': res,'ShareLink':ShareLink})

    if 'client' in data:
        res = SBCShareManages.GetShareInfo(ShareLink)
        return JsonResponse({'res': res})

    return render(request,'SBCShare/SBCShare.html')