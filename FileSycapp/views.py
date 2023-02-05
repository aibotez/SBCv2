from django.shortcuts import render
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from SBC import LoginVerfiy

from django.http import HttpResponseRedirect
from SBC import GetUserPath
from django.http import HttpResponse,JsonResponse
import os,json,hashlib
# from FileSycManager import FileSycManager
from . import FileSycManager
# Create your views here.


def str_trans_to_md5(src):
    src = src.encode("utf-8")
    myMd5 = hashlib.md5()
    myMd5.update(src)
    myMd5_Digest = myMd5.hexdigest()
    return myMd5_Digest
def GetAllFilesfromFolder(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    res = {'errnor':'1'}
    FileInfo = json.loads(request.body)
    path = FileInfo['path']
    getuserpath = GetUserPath.GetUserPath()
    path = getuserpath.getuserserpath(LoginRes['useremail'],path)
    Files = {}
    for root, dirs, files in os.walk(path):
        root += '/'
        root = root.replace('\\', '/').replace('//', '/')
        fapath = root.replace(path, '')
        if '__pycache__' not in fapath:
            for i in files:
                fepath = path + fapath + i
                FileInfo = {}
                FileInfo['fapath'] = fepath.replace(path, '/')
                FileInfo['fepath'] = fepath
                FileInfo['size'] = os.path.getsize(fepath)
                FileInfo['date'] = os.stat(fepath).st_mtime
                Files[str_trans_to_md5(fepath)] = FileInfo
    return JsonResponse(Files)

def CheckSBCFile(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    FileInfo = json.loads(request.body)
    FileInfo['useremail'] = LoginRes['useremail']
    FileCheck = FileSycManager.FileSycManager().checkFile(FileInfo)
    return JsonResponse(FileCheck)
