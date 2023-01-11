import json

from django.shortcuts import render
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from SBC import LoginVerfiy
from django.http import HttpResponseRedirect
from django.http import HttpResponse,JsonResponse
from SBC import GetUserPath
from SBC import UserManage
from FileDownUpapp import FileDownUp
# Create your views here.

# @require_POST
def FileDown(request):
    # print(request.POST)
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        downinfo = request.POST['downinfo']
    else:
        downinfo = request.GET['downinfo']
    getuserpath = GetUserPath.GetUserPath()
    downinfo = getuserpath.GetDownPath(downinfo,LoginRes)
    FileDowUpCOm = FileDownUp.FileDU()
    res = FileDowUpCOm.Down(downinfo)
    return res
def FileDown1(request):
    # print(request.POST)
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')

    # print(request.body)

    if request.method == 'POST':
        downinfo = json.loads(request.body)
        downinfo = downinfo['downinfo']
    else:
        downinfo = request.GET['downinfo']
    downinfo = json.dumps(downinfo)
    getuserpath = GetUserPath.GetUserPath()
    downinfo = getuserpath.GetDownPath(downinfo,LoginRes)
    print(downinfo)
    FileDowUpCOm = FileDownUp.FileDU()
    res = FileDowUpCOm.Down1(downinfo)
    return res


@require_POST
def CheckFile(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    # print(json.loads(request.body))
    # print(request.POST)
    FileSize = int(request.POST['FileSize'])
    usermange = UserManage.usermange()
    if usermange.Capisfull(LoginRes['useremail'],FileSize):
        return HttpResponse('FULL')
    FileDowUpCOm = FileDownUp.FileUp()
    res = FileDowUpCOm.UpfileCheck(request.POST.dict(),LoginRes['useremail'])
    return JsonResponse(res)

@require_POST
def FileUp(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    # print(request.POST)
    FileSize = int(request.POST['FileSize'])
    usermange = UserManage.usermange()
    if usermange.Capisfull(LoginRes['useremail'],FileSize):
        return HttpResponse('FULL')
    file_obj = request.FILES.get("file")
    FileDowUpCOm = FileDownUp.FileUp()
    FileDowUpCOm.Upfile(request.POST.dict(),LoginRes['useremail'],file_obj)
    # # print(request.FILES.get("file"))
    # file_obj = request.FILES.get("file")
    # FileMd5 = request.POST['FileMd5']
    # # print(file_obj)
    # print(FileMd5)
    # return HttpResponse('1')
    # with open('static/uptest/' + file_obj.name, "wb") as f:
    #     for chunk in file_obj.chunks(chunk_size=2 * 1024 * 1024):
    #         f.write(chunk)
    return HttpResponse('1')
