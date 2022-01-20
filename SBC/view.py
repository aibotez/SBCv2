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
def filesget(path):

    navpath = path[1:-1]
    navpathlist = navpath.split('/')

    lj = 'C:/doucment/gitstock/SBCtest/SBCtestFolder'+path
    dirshome = os.listdir(lj)
    fesdata=[]
    for i in dirshome:
        febig = '-'
        isdir = 1
        imgpath = '/static/img/foldersm.png'
        if not os.path.isdir(lj + i):
            febig = os.path.getsize(lj + i)
            febig = size_format(febig)
            isdir = 0
            imgpath = '/static/img/wj.jfif'
        fesdata.append({
            'filename':i,
            'filelj':lj+i+'/',
            'big':febig,
            'date':getdate(lj+i),
            'isdir':isdir,
            'imgpath':imgpath,
        })
    return fesdata

def getdate(fie):
    statbuf = os.stat(fie)
    date=time.strftime('%Y-%m-%d %H:%M', time.localtime(statbuf.st_mtime))
    # date= statbuf.st_mtime
    return date
def Home(request):
    if LoginVerfiy.LoginVerfiy().verifylogin(request):
        return HttpResponseRedirect('/login/')
    path = "/plugins/"
    data=filesget(path)
    # data = [{'filename':'abc.pdf','filelj':'home/asg','big':'20.5M','date':'2021-08-09'},
    #         {'filename':'dirs1','filelj':'home/asg','big':'127KB','date':'2019-10-12'},
    #         ]
    filelj = ['home','asg']
    return render(request, "home/home1.html",locals())
# @require_POST
def home(request):
    print(request.POST['ids'])
    path =request.POST['ids']
    path = path.replace('C:/doucment/gitstock/SBCtest/SBCtestFolder','')
    print(path)
    # path = "/plugins/flot/"
    data=filesget(path)
    return render(request, "home/FileList.html", locals())
