from django.shortcuts import render
from SBC import LoginVerfiy
from django.http import HttpResponse,JsonResponse
from django.http import HttpResponseRedirect
import json,re
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


def GetBaiduNetUserInfo(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    manage = BaiduNetManage.manage()
    BaiduNetUserInfo = manage.GetBaiduNetUserInfo(LoginRes)
    return JsonResponse(BaiduNetUserInfo)

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


def GetFiles(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
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
    return JsonResponse({'navlist':navlist,'navlastpath':navlastpath,'list':data})
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
    res = manage.BaiduNetSaveUser(LoginRes,request.POST.get('usercookie'))
    # print(res)
    return JsonResponse({'res':res})

@require_POST
def BaiduNetQuitLogin(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    manage = BaiduNetManage.manage()
    res = manage.BaiduNetQuit(LoginRes, request.POST.get('usercookie'))
    return JsonResponse({'res': res})
@require_POST
def GetBDDownLink(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    data = request.POST
    # print(data,data['fepath'])
    manage = BaiduNetManage.manage()
    DownLink = manage.GetBaiduNetDownLinkFromPan(data['fepath'],LoginRes)
    FileSize = int(re.findall(".*size=(\d+)&.*",DownLink)[0])
    return JsonResponse({'errno':'0','DownLink':DownLink,'FileSize':FileSize})




from django.http import StreamingHttpResponse,FileResponse
from django.utils.encoding import escape_uri_path
import requests
def Down(FileInfo):

    heades = {
        'User-Agent': 'netdisk;P2SP;3.0.0.127',
        # 'Connection': 'Keep - Alive',
        # 'Host': 'bdcm01.baidupcs.com',
        # 'Range': 'bytes=0-102400'
    }
    def file_iterator(chunk_size=400 * 1024):
        # heades['Range'] = 'bytes={}-{}'.format(str(0), str(1024))
        # with requests.get(FileInfo['url'],headers=heades,stream=True) as req:
        #     for chunk in req.iter_content(chunk_size=chunk_size):
        #         if chunk:
        #             print(len(chunk))
        #             yield chunk
        #         else:
        #             print(chunk)
        #             break

        SizeOffet = -1
        while True:
            if SizeOffet>FileInfo['FileSize']:
                break
            else:
                heades['Range'] = 'bytes={}-{}'.format(str(SizeOffet+1),str(SizeOffet+chunk_size))

                res = requests.get(FileInfo['url'],headers=heades).content
                # print(len(res))
                # break
                SizeOffet = SizeOffet + chunk_size
                yield res


    the_file_name = FileInfo['FileName']
    # print(the_file_name,the_file_path)
    # response = FileResponse(file_iterator(the_file_name))
    response = StreamingHttpResponse(file_iterator())
    response = FileResponse(response)
    response['Content-Type'] = 'application/octet-stream'
    response['content-length'] = FileInfo['FileSize']
    # response['Content-Disposition'] = 'attachment;filename="{0}"'.format(wjname)
    response["Content-Disposition"] = "attachment; filename*=UTF-8''{}".format(escape_uri_path(the_file_name))
    return response

from django.shortcuts import redirect
def reD(request):
    FileInfo = {
        'url':request.POST['url'],
        'FileName':request.POST['FileName'],
        'FileSize':int(request.POST['FileSize'])
    }
    # print(request.POST['url'])
    res = Down(FileInfo)
    return res
    # return HttpResponse(request.POST['url'])
