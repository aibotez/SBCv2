
from SBC import FileType
from django.shortcuts import render
import os
from django.contrib.auth.decorators import login_required
from SBC import LoginVerfiy
from django.http import HttpResponse,JsonResponse
from django.http import HttpResponseRedirect
from SBC import GetUserPath

# Create your views here.


def preview(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    getuserpath = GetUserPath.GetUserPath()

    req = {'path':request.GET['filepath']}
    path = getuserpath.userpath(req,LoginRes)[1]
    FiletypeJudge = FileType.FileType()
    filetype = FiletypeJudge.GetFileType(path)
    if filetype == 'image':
        image_data = open(path, "rb").read()
        return HttpResponse(image_data, content_type="image/png")
