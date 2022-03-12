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
    ShareFileInfo = json.loads(list(request.POST.keys())[0])
    # print(ShareFileInfo)
    req = request.POST.dict()
    CurUrl = request.get_host()
    SBCShareManages = SBCShareManage.ShareManage()
    res = SBCShareManages.CreatShareUrl(ShareFileInfo,LoginRes,CurUrl)
    return JsonResponse({'res':res})
    # return HttpResponse()

def SBCShareShow(request):
    return render(request,'SBCShare/SBCShare.html')