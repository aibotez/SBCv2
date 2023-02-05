from django.shortcuts import render
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from SBC import LoginVerfiy

from django.http import HttpResponseRedirect
from SBC import GetUserPath
from django.http import HttpResponse,JsonResponse
import os,json
# Create your views here.


def GetAllFilesfromFolder(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    res = {'errnor':'1'}
    FileInfo = json.loads(request.body)
    path = FileInfo['path']
    getuserpath = GetUserPath.GetUserPath()
    path = getuserpath.getuserserpath(LoginRes['useremail'],path)
    Files = []
    for root, dirs, files in os.walk(path):
        root += '/'
        root = root.replace('\\', '/').replace('//', '/')
        fapath = root.replace(path, '')
        for i in files:
            fepath = path + fapath + i
            FileInfo = {}
            FileInfo['fapath'] = fepath.replace(path, '/')
            FileInfo['fepath'] = fepath
            FileInfo['size'] = os.path.getsize(fepath)
            FileInfo['date'] = os.stat(fepath).st_mtime
            Files.append(FileInfo)
    return JsonResponse({'Files':Files})