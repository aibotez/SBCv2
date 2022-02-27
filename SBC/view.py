from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import os
from django.contrib.auth.decorators import login_required
from SBC import LoginVerfiy
from django.http import HttpResponse,JsonResponse
from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse,FileResponse
from urllib import parse
import shutil,json,io
import socket,os,time,threading
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from SBC import FileOper
from SBC import UserManage
from PIL import Image

# from SBC import FileDownUp

def size_format(size):
    if size < 1024:
        return '%i' % size + 'size'
    elif 1024 <= size < 1024*1024:
        return '%.1f' % float(size/1024) + 'KB'
    elif 1024*1024 <= size < 1024*1024*1024:
        return '%.1f' % float(size/(1024*1024)) + 'MB'
    elif 1024*1024*1024 <= size < 1024*1024*1024*1024:
        return '%.1f' % float(size/(1024*1024*1024)) + 'GB'
    elif 1024*1024*1024*1024 <= size:
        return '%.1f' % float(size/(1024*1024*1024*1024)) + 'TB'
def filesget(paths):
    path = paths[0]
    serverpath = paths[1]
    navpath = path[1:-1]
    navpathlist = navpath.split('/')
    navpaths = []
    s = '/'
    for i in navpathlist:
        s = s+i+'/'
        navpaths.append({'navname':i,'path':s})

    dirshome = os.listdir(serverpath)
    fesdata=[]
    for i in dirshome:
        filesonserver = serverpath + i
        fileson = path + i
        filesize = '-'
        isdir = 1
        filepath = fileson+'/'
        imgpath = '/static/img/foldersm.png'
        if not os.path.isdir(filesonserver):
            filesize = os.path.getsize(filesonserver)
            filesize = size_format(filesize)
            isdir = 0
            imgpath = '/static/img/wj.jfif'
            filepath = fileson
        fesdata.append({
            'filename':i,
            'filelj':filepath,
            'big':filesize,
            'date':getdate(filesonserver),
            'isdir':isdir,
            'imgpath':imgpath,
        })
    return [fesdata,navpaths]

def getdate(fie):
    statbuf = os.stat(fie)
    date=time.strftime('%Y-%m-%d %H:%M', time.localtime(statbuf.st_mtime))
    # date= statbuf.st_mtime
    return date
from SBC import GetUserPath
def Home(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    getuserpath = GetUserPath.GetUserPath()
    req = request.GET.dict()
    paths = getuserpath.userpath(req,LoginRes)
    req['path'] = paths[0]
    datas=filesget(paths)
    data=datas[0]
    datajson = json.dumps(data)
    # print(datajson)
    navlist = datas[1]
    navlastpath = navlist[-1]['path']
    # print(navlastpath)
    return render(request, "home/home1.html",locals())
# @require_POST
def FileList(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    getuserpath = GetUserPath.GetUserPath()
    # if request.method == 'GET':
    #     pass
    req = {'path':request.POST['ids']}
    paths = getuserpath.userpath(req,LoginRes)
    datas=filesget(paths)
    data=datas[0]
    navlist = datas[1]
    navlastpath = navlist[-1]['path']
    # uesremail = LoginRes['uesremail']
    # print(request.POST['ids'])
    # path = path.replace('C:/doucment/gitstock/SBCtest/SBCtestFolder','')
    # print(path)
    # path = "/plugins/flot/"
    # data=filesget(paths)

    return render(request, "home/FileList.html", locals())

def getdirsize(dir):
    size = 0
    for root, dirs, files in os.walk(dir):
        size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
    return size
import shutil
@require_POST
def DelFiles(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    DelFilesInfo = {}
    DelFilesStr = request.POST.dict()
    for k in DelFilesStr.keys():
        DelFilesInfo = json.loads(k)

    DelFilesList = DelFilesInfo['data']
    getuserpath = GetUserPath.GetUserPath()
    for i in DelFilesList:
        path = i['fepath']
        userPath = getuserpath.getuserserpath(LoginRes['useremail'],path)
        usermange = UserManage.usermange()

        try:
            # print(userPath)
            # print(i)
            if i['feisdir']:
                shutil.rmtree(userPath)
                DirsSize = getdirsize(userPath)
                usermange.DelUsedCap(LoginRes['useremail'],DirsSize)
            else:
                os.remove(userPath)
                usermange.DelUsedCap(LoginRes['useremail'],os.path.getsize(userPath))
        except Exception as e:
            print(e)

    return HttpResponse('ok')

@require_POST
def ReName(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    ReNameInfo = request.POST.dict()
    fileOper = FileOper.FileOper()
    # print(request.POST)

    getuserpath = GetUserPath.GetUserPath()
    userPath = getuserpath.getuserserpath(LoginRes['useremail'], ReNameInfo['OldNamePath'])
    res = fileOper.Rename(userPath ,ReNameInfo['NewName'])
    return HttpResponse(res)


@require_POST
def netOper(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    netoper = FileOper.netOper()
    res = netoper.netOperMain(LoginRes['useremail'],request.POST.dict())
    return HttpResponse(res)
# @require_POST
# def FileDown(request):
#     # print(request.POST)
#     LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
#     if LoginRes['res']:
#         return HttpResponseRedirect('/login/')
#     if request.method == 'POST':
#         downinfo = request.POST['downinfo']
#     else:
#         downinfo = request.GET['downinfo']
#     getuserpath = GetUserPath.GetUserPath()
#     downinfo = getuserpath.GetDownPath(downinfo,LoginRes)
#     FileDowUpCOm = FileDownUp.FileDU()
#     res = FileDowUpCOm.Down(downinfo)
#     return res
#
# @require_POST
# def FileUp(request):
#     LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
#     if LoginRes['res']:
#         return HttpResponseRedirect('/login/')
#     # print(request.FILES.get("file"))
#     file_obj = request.FILES.get("file")
#     # print(file_obj)
#     with open('static/uptest/' + file_obj.name, "wb") as f:
#         for chunk in file_obj.chunks(chunk_size=2 * 1024 * 1024):
#             f.write(chunk)
#     return HttpResponse('1')

#os.symlink(src,dst)创建软链接
