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
from PIL import Image

from SBC import FileDownUp

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
    datas=filesget(paths)
    data=datas[0]
    navlist = datas[1]
    navlastpath = navlist[-1]['path']
    print(navlastpath)
    return render(request, "home/home1.html",locals())
# @require_POST
def home(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    getuserpath = GetUserPath.GetUserPath()
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

@require_POST
def FileUp(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    # print(request.FILES.get("file"))
    file_obj = request.FILES.get("file")
    print(file_obj)
    # with open('static/uptest/' + file_obj.name, "wb") as f:
    #     for chunk in file_obj.chunks(chunk_size=2 * 1024 * 1024):
    #         f.write(chunk)
    return HttpResponse('1')

#os.symlink(src,dst)创建软链接
