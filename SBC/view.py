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


def filesget(path):
    lj = '/static'+path
    dirshome = os.listdir(lj)
    

def Home(request):
    if LoginVerfiy.LoginVerfiy().verifylogin(request):
        return HttpResponseRedirect('/login/')

    data = [{'filename':'abc.pdf','filelj':'home/asg','big':'20.5M','date':'2021-08-09'},
            {'filename':'dirs1','filelj':'home/asg','big':'127KB','date':'2019-10-12'},
            ]
    filelj = ['home','asg']
    return render(request, "home/home1.html",locals())


