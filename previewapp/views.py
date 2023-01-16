
from SBC import FileType
from django.shortcuts import render
import os
from django.contrib.auth.decorators import login_required
from SBC import LoginVerfiy
from django.http import HttpResponse,JsonResponse
from django.http import HttpResponseRedirect
from SBC import GetUserPath
import base64,json

# Create your views here.

def GetFeBase64(path):
    with open(path, 'rb') as f:
        # lsf = base64.b64decode(f.read())
        febase64 = base64.b64encode(f.read()).decode()
        # imgbase64Url = "data:image/{};base64,".format(imgtype) + imgbase64
        return febase64
def preview(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    getuserpath = GetUserPath.GetUserPath()

    if request.method == 'GET':
        req = {'path':request.GET['filepath']}
    else:
        prep = json.loads(request.body)
        # print(json.loads(request.body),type(json.loads(request.body)))
        req = {'path': prep['filepath']}
    path = getuserpath.userpath(req,LoginRes)[1]
    FiletypeJudge = FileType.FileType()
    filetype = FiletypeJudge.GetFileType(path)[0]
    if filetype == 'image':

        image_data = open(path, "rb").read()

        return HttpResponse(image_data, content_type="image/png")
    if filetype == 'pdf':
        # pdfbase64 = "data:application/pdf;base64," + GetFeBase64(path)
        pdfbase64 = GetFeBase64(path)
        # return HttpResponseRedirect('/pdfviewer.html')
        return render(request, "preview/pdfviewer.html",locals())
