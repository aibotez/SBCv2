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

def size_format(size):
    if size < 1000:
        return '%i' % size + 'size'
    elif 1000 <= size < 1000000:
        return '%.1f' % float(size/1000) + 'KB'
    elif 1000000 <= size < 1000000000:
        return '%.1f' % float(size/1000000) + 'MB'
    elif 1000000000 <= size < 1000000000000:
        return '%.1f' % float(size/1000000000) + 'GB'
    elif 1000000000000 <= size:
        return '%.1f' % float(size/1000000000000) + 'TB'
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
        imgpath = '/static/img/foldersm.png'
        if not os.path.isdir(filesonserver):
            filesize = os.path.getsize(filesonserver)
            filesize = size_format(filesize)
            isdir = 0
            imgpath = '/static/img/wj.jfif'
        fesdata.append({
            'filename':i,
            'filelj':fileson+'/',
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
    # uesremail = LoginRes['uesremail']
    # print(request.POST['ids'])
    # path = path.replace('C:/doucment/gitstock/SBCtest/SBCtestFolder','')
    # print(path)
    # path = "/plugins/flot/"
    # data=filesget(paths)

    return render(request, "home/FileList.html", locals())

#os.symlink(src,dst)创建软链接
