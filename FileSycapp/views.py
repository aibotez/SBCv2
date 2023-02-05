from django.shortcuts import render
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from SBC import LoginVerfiy

from django.http import HttpResponseRedirect
from SBC import GetUserPath
from django.http import HttpResponse,JsonResponse
import os,json,hashlib
# from FileSycManager import FileSycManager
from . import FileSycManager
from SBC import UserManage
# Create your views here.


def str_trans_to_md5(src):
    src = src.encode("utf-8")
    myMd5 = hashlib.md5()
    myMd5.update(src)
    myMd5_Digest = myMd5.hexdigest()
    return myMd5_Digest
def getfileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename, "rb")
    while True:
        b = f.read(2*1024*1024)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()
def GetAllFilesfromFolder(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    res = {'errnor':'1'}
    FileInfo = json.loads(request.body)
    path = FileInfo['path']
    getuserpath = GetUserPath.GetUserPath()
    Serpath0 = getuserpath.getuserserpath(LoginRes['useremail'],path)
    Files = {}
    for root, dirs, files in os.walk(Serpath0):
        root += '/'
        root = root.replace('\\', '/').replace('//', '/')
        fapath = root.replace(Serpath0, '')
        if '__pycache__' not in fapath:
            for i in files:
                fepath = Serpath0 + fapath + i
                FileInfo = {}
                FileInfo['fapath'] = fepath.replace(Serpath0, '/')
                FileInfo['fapath1'] = fapath
                FileInfo['fepath'] = path[0:-1] + fepath.replace(Serpath0, '/')
                FileInfo['size'] = os.path.getsize(fepath)
                FileInfo['date'] = os.stat(fepath).st_mtime
                FileInfo['fename'] = os.path.basename(fepath)
                FileInfo['filemd5'] = getfileMd5(fepath)
                Files[str_trans_to_md5(FileInfo['fepath'])] = FileInfo
    return JsonResponse(Files)

def CheckSBCFile(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    FileInfo = json.loads(request.body)
    FileInfo['useremail'] = LoginRes['useremail']
    FileCheck = FileSycManager.FileSycManager().checkFile(FileInfo)
    return JsonResponse(FileCheck)

def Upfile(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    FileInfo = request.POST['FileInfo']
    FileInfo = json.loads(FileInfo)
    FileInfo['useremail'] = LoginRes['useremail']
    FileSize = int(FileInfo['FileSize'])
    usermange = UserManage.usermange()
    if usermange.Capisfull(LoginRes['useremail'],FileSize):
        return HttpResponse('FULL')
    file_obj = request.FILES.get("file")
    FileUp = FileSycManager.FileSycManager().UpFile(FileInfo,file_obj)
    return JsonResponse({'res':FileUp})
