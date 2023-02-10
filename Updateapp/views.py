from django.shortcuts import render
import shutil,json,io
import socket,os,time,threading,hashlib
from django.http import StreamingHttpResponse,FileResponse
from django.http import HttpResponse,JsonResponse
from django.utils.encoding import escape_uri_path
from django.views.decorators.http import require_GET, require_http_methods, require_POST
# Create your views here.


def GetMaxVer(client):
    path = ''
    if client == 'windows':
        path ='static/Client/Windows'
    felist = os.listdir(path)
    Vers = [i.split('_')[1] for i in felist]
    Versint = [float('0.'+i.replace('.','')) for i in Vers]
    VerMax = Versint[-1]
    VerStrMax = ''
    for i in Vers:
        if float('0.'+i.replace('.','')) == VerMax:
            VerStrMax = i
    return {'Ver':VerStrMax,'Verint':VerMax}

def GetCurVer(request):
    if request.method == 'GET':
        client = request.GET['client']
    else:
        client = request.POST['client']
    CurVer = GetMaxVer(client)
    return JsonResponse(CurVer)

def GetFileMd5(filename):
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
def file_iterator(file_name, chunk_size=20 * 1024 * 1024):
    with open(file_name, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break
def DownClient(request):
    if request.method == 'GET':
        client = request.GET['client']
    else:
        client = request.POST['client']
    CurVer = GetMaxVer(client)
    path = 'static/Client/Windows/SBC_{}_.7z'.format(CurVer['Ver'])
    the_file_name = 'SBC_{}_.7z'.format(CurVer['Ver'])
    the_file_path = path
    # print(the_file_name,the_file_path)
    # response = FileResponse(file_iterator(the_file_name))
    response = StreamingHttpResponse(file_iterator(the_file_path))
    response = FileResponse(response)
    response['Content-Type'] = 'application/octet-stream'
    response['FileMd5'] = GetFileMd5(the_file_path)
    response['size'] = os.path.getsize(the_file_path)
    response['FileName'] = the_file_name
    response['content-length'] = os.path.getsize(the_file_path)
    # response['Content-Disposition'] = 'attachment;filename="{0}"'.format(wjname)
    response["Content-Disposition"] = "attachment; filename*=UTF-8''{}".format(escape_uri_path(the_file_name))
    return response
