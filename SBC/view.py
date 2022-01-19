from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
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




def Home(request):
    if LoginVerfiy.LoginVerfiy().verifylogin(request):
        return HttpResponseRedirect('/login/')

    data = [{'file-name':'abc.pdf','file-lj':'home/asg'},{'file-name':'dirs1','file-lj':'home/asg'}]
    filelj = ['home','asg']
    return render(request, "home/home1.html",locals())


