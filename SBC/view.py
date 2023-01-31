from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import os,hashlib
from django.contrib.auth.decorators import login_required
from SBC import LoginVerfiy
from django.http import HttpResponse,JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.http import StreamingHttpResponse,FileResponse
from urllib import parse
import shutil,json,io
import socket,os,time,threading
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from SBC import FileOper
from SBC import UserManage
import base64
import mimetypes
from PIL import Image
from SBC import FileType
from UserFileRecordapp import UserFileRecordManage
from SBCShareapp import SBCShareManage
from io import BytesIO

SBCShareManages = SBCShareManage.ShareManage()
# from SBC import FileDownUp

def size_format(size):
    if size < 1024:
        return '%i' % size + 'size'
    elif 1024 <= size < 1024*1024:
        return '%.1f' % float(size/1024) + 'KB'
    elif 1024*1024 <= size < 1024*1024*1024:
        return '%.1f' % float(size/(1024*1024)) + 'MB'
    elif 1024*1024*1024 <= size < 1024*1024*1024*1024:
        return '%.1f' % float(size/(1024*1024*1024)) + 'GB'
    elif 1024*1024*1024*1024 <= size:
        return '%.1f' % float(size/(1024*1024*1024*1024)) + 'TB'


def deal_inspect_img(base64_data,imgtype):
    """裁剪base64字符串的图片"""
    byte_data = base64.b64decode(base64_data)
    # BytesIO 对象
    image_data = io.BytesIO(byte_data)
    # 得到Image对象
    img = Image.open(image_data)
    # 裁剪图片(左，上，右，下)，笛卡尔坐标系
    # img2 = img.crop((962, 485, 1897, 810))
    img2 = img.resize((50, 50), Image.ANTIALIAS)
    # BytesIO 对象
    imgByteArr = io.BytesIO()
    # 写入BytesIO对象
    img2.save(imgByteArr, format=imgtype)
    # 获得字节
    imgByteArr = imgByteArr.getvalue()
    base64_str = base64.b64encode(imgByteArr).decode()
    return base64_str

def GetImgconBase64(fepath,imgtype):
    with open(fepath, 'rb') as f:
        # lsf = base64.b64decode(f.read())
        imgbase64 = base64.b64encode(f.read()).decode()
        imgbase64 = deal_inspect_img(imgbase64, imgtype)
        imgbase64Url = "data:image/{};base64,".format(imgtype) + imgbase64
        return imgbase64Url
def GetImgConPath1(fepath):
    try:
        filtypeOb = FileType.FileType()
        fetype = filtypeOb.GetFileType(fepath)
        imgtype = fetype[1]
        return GetImgconBase64(fepath, imgtype)
    except Exception as e:
        print(e)
    return '/static/img/wj.jfif'
def GetImgConPath(fepath):
    filtypeOb = FileType.FileType()
    # fetypes = mimetypes.guess_type(fepath)
    # print(fepath,fetypes)
    try:
        fetype = filtypeOb.GetFileType(fepath)
        # fetype = fetypes[0].split('/')[0]
        if fetype[0] == 'image':
            path = '/static/img/filecon/imgcon.jpg'
            return [path,'img']
            # imgtype = fetype[1]
            # return GetImgconBase64(fepath,imgtype)
        if fetype[0] == 'pdf':
            path = '/static/img/filecon/pdfcon.jpg'
            return [path,'pdf']
        if fetype[0] == 'word':
            path = '/static/img/filecon/wordcon.jpg'
            return [path,'word']
        if fetype[0] == 'ppt':
            path = '/static/img/filecon/pptcon.jpg'
            return [path,'ppt']
        if fetype[0] == 'excel':
            path = '/static/img/filecon/excelcon.jpg'
            return [path,'excel']
        if fetype[0] == 'zip':
            path = '/static/img/filecon/zipcon.png'
            return [path,'zip']
        if fetype[0] == 'html':
            path = '/static/img/filecon/htmlcon.jpg'
            return [path,'html']
        if fetype[0] == 'exe':
            path = '/static/img/filecon/execon.jpg'
            return [path,'exe']
    except Exception as e:
        print(e)
    return ['/static/img/wj.jfif','other']

def GetFileInfo(path):
    # path = paths[0]
    serverpath = path
    FileJu = GetImgConPath(serverpath)
    imgpath = FileJu[0]
    fetype = FileJu[1]
    fedata={
        'filename': os.path.basename(serverpath),
        'fename':os.path.basename(serverpath),

        # 'filelj': path,
        # 'big': filesize1,
        'size': os.path.getsize(serverpath),
        'date': getdate(serverpath),
        'isdir': 0,
        'imgpath': imgpath,
        'fetype': fetype,
    }
    return fedata
def filesget(paths):
    path = paths[0]
    serverpath = paths[1]
    navpath = path[1:-1]
    navpathlist = navpath.split('/')
    navpaths = []
    s = '/'
    for i in navpathlist:
        s = s+i+'/'
        Npath = base64.encodebytes(s.encode('utf8')).decode()
        Npath = Npath.replace('\n', '')
        navpaths.append({'navname':i,'path':s,'pathId':Npath})

    dirshome = os.listdir(serverpath)
    # dirshome.sort(key=lambda file: os.path.getctime(os.path.join(serverpath, file)))
    fesdata=[]
    imgFiles = []
    dirlist = []
    felist = []
    for i in dirshome:
        filesonserver = serverpath + i
        fileson = path + i
        filesize = -1
        filesize1 = '-'
        isdir = 1
        filepath = fileson+'/'
        imgpath = '/static/img/foldersm.png'
        fetype = 'folder'
        if not os.path.isdir(filesonserver):
            filesize = os.path.getsize(filesonserver)
            filesize1 = size_format(filesize)
            isdir = 0
            FileJu = GetImgConPath(filesonserver)
            imgpath = FileJu[0]
            fetype = FileJu[1]
            if 'imgcon.jpg' in imgpath:
                imgFiles.append({'fepath':fileson})
            # imgpath = '/static/img/wj.jfif'
            filepath = fileson
        filepath = base64.encodebytes(filepath.encode('utf8')).decode()
        filepath = filepath.replace('\n','')
        feinfo = {
            'filename':i,
            'filelj':filepath,
            'big':filesize1,
            'size':filesize,
            'date':getdate(filesonserver),
            'date0':os.stat(filesonserver).st_mtime,
            'isdir':isdir,
            'imgpath':imgpath,
            'fetype':fetype,
        }
        fesdata.append(feinfo)
        if os.path.isdir(filesonserver):
            dirlist.append(feinfo)
        else:
            felist.append(feinfo)
    # return [{'dir':dirlist,'fe':felist}, navpaths, imgFiles]
    return [fesdata,navpaths,imgFiles]

def getfileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename, "rb")
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()

from SBC import GetUserPath
@require_POST
def GetFileMd5(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    FeMd5 = None
    FileInfo = json.loads(request.body)
    if 'shareinfo' in FileInfo:
        path = SBCShareManages.GetShareSerPath(FileInfo['shareinfo'])
        FeMd5 = getfileMd5(path)
    else:
        print('NoShare')
        getuserpath = GetUserPath.GetUserPath()
        req = {'path':FileInfo['path']}
        path = getuserpath.userpath(req,LoginRes)
        FeMd5 = getfileMd5(path[1])
    # return HttpResponse(FeMd5)
    return JsonResponse({'error':0,'md5':FeMd5})

def getdate(fie):
    statbuf = os.stat(fie)
    date=time.strftime('%Y-%m-%d %H:%M', time.localtime(statbuf.st_mtime))
    # date= statbuf.st_mtime
    return date

def Home(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    getuserpath = GetUserPath.GetUserPath()
    req = request.GET.dict()
    paths = getuserpath.userpath(req,LoginRes)
    req['path'] = paths[0]
    datas=filesget(paths)
    data=datas[0]
    datajson = json.dumps(data)
    # print(datajson)
    navlist = datas[1]
    navlastpath = navlist[-1]['path']
    # print(navlastpath)
    usermanage = UserManage.usermange()
    UserUsedCap = usermanage.GetUserUsedCap(LoginRes['useremail'])
    response = render(request, "home/home2.html",locals())
    response['x-content-type-options'] = 'nosniff'
    response['Content-Type'] = 'text/html; charset=UTF-8'
    response['Cache-control'] = 'no-cache'
    return response
# @require_POST
def FileList(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    getuserpath = GetUserPath.GetUserPath()
    # if request.method == 'GET':
    #     pass
    req = {'path':request.POST['ids']}
    paths = getuserpath.userpath(req,LoginRes)
    datas=filesget(paths)
    data=datas[0]
    navlist = datas[1]
    imgFiles = datas[2]
    navlastpath = navlist[-1]['path']
    # uesremail = LoginRes['uesremail']
    # print(request.POST['ids'])
    # path = path.replace('C:/doucment/gitstock/SBCtest/SBCtestFolder','')
    # print(path)
    # path = "/plugins/flot/"
    # data=filesget(paths)
    usermanage = UserManage.usermange()
    UserUsedCap = usermanage.GetUserUsedCap(LoginRes['useremail'])
    response = render(request, "home/FileList2.html", locals())
    response['x-content-type-options'] = 'nosniff'
    response['Content-Type'] = 'text/html; charset=UTF-8'
    response['Cache-control'] = 'no-cache'
    return response


def GetAllFiles(paths):
    Files = []
    path = paths[1].replace('\\', '/')
    for root, dirs, files in os.walk(path):
        root += '/'
        root = root.replace('\\', '/').replace('//','/')
        fapath = root.replace(path, '')
        for i in files:
            fepath = root + i

            FileInfo = GetFileInfo(fepath)
            FileInfo['fepath'] = paths[0]+fapath+i
            FileInfo['fapath'] = fapath
            Files.append(FileInfo)
    return Files
@require_POST
def GetAllFilesfromFolder(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    res = {'errnor':'1'}
    getuserpath = GetUserPath.GetUserPath()
    req = {'path':request.POST['path']}
    paths = getuserpath.userpath(req,LoginRes)
    fileinfo = GetAllFiles(paths)
    res = {'Files':fileinfo}
    return JsonResponse(res)


@require_POST
def GetFileListbyClient(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    res = {'errnor':'1'}
    getuserpath = GetUserPath.GetUserPath()
    req = {'path':request.POST['path']}
    paths = getuserpath.userpath(req,LoginRes)
    datas=filesget(paths)
    res['errnor'] = '0'
    res['FileList'] = datas[0]
    res['Nav'] = datas[1]
    res['imgFiles'] = datas[2]
    return JsonResponse(res)



def GetFilePorper(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    File = json.loads(request.body)
    getuserpath = GetUserPath.GetUserPath()
    paths = getuserpath.userpath(File,LoginRes)
    serverpath = paths[1]
    size = 0
    FolderNums = -1
    FileNUms = 0
    if File['isdir']:
        for root, dirs, files in os.walk(serverpath):
            FileNUms += len(files)
            FolderNums += 1
            size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
    else:
        size = File['size']
    statbuf = os.stat(serverpath)
    Modfdate=time.strftime('%Y-%m-%d %H:%M', time.localtime(statbuf.st_mtime))
    Crefdate = time.strftime('%Y-%m-%d %H:%M', time.localtime(statbuf.st_ctime))
    res = File
    res['mtime'] = Modfdate
    res['ctime'] = Crefdate
    res['size'] = size
    res['FolderNums'] = FolderNums
    res['FileNUms'] = FileNUms
    return JsonResponse(res)



def getdirsize(dir):
    size = 0
    for root, dirs, files in os.walk(dir):
        size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
    return size
import shutil
@require_POST
def DelFiles(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    DelFilesInfo = {}
    if 'client' in json.loads(request.body):
        DelFilesInfo = json.loads(request.body)
    else:
        DelFilesStr = request.POST.dict()
        print(json.loads(request.body))
        for k in DelFilesStr.keys():
            DelFilesInfo = json.loads(k)

    DelFilesList = DelFilesInfo['data']
    getuserpath = GetUserPath.GetUserPath()
    for i in DelFilesList:
        path = i['fepath']
        userPath = getuserpath.getuserserpath(LoginRes['useremail'],path)
        usermange = UserManage.usermange()

        try:
            # print(userPath)
            # print(i)
            if i['feisdir']:

                DirsSize = getdirsize(userPath)
                shutil.rmtree(userPath)
                usermange.DelUsedCap(LoginRes['useremail'], DirsSize)
            else:
                DirsSize = os.path.getsize(userPath)
                os.remove(userPath)
                usermange.DelUsedCap(LoginRes['useremail'],DirsSize)

            userfilerecordmanage = UserFileRecordManage.userfilerecordmanage()
            userfilerecordmanage.DelRecord(LoginRes['useremail'],path)
        except Exception as e:
            print(e)

    return HttpResponse('ok')

@require_POST
def GetImgCon(request):
    # print(request.body)
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    # imgdict = json.loads(list(imgdict.keys())[0])
    imgdict = json.loads(request.body.decode('utf-8'))
    if 'fepath' not in request.body.decode('utf-8'):
        imgdict['imgdata'] = base64.decodebytes(imgdict['imgdata'].encode('utf8')).decode()
        imgdict['imgdata'] = json.loads(imgdict['imgdata'])
    # print(imgdict)
    getuserpath = GetUserPath.GetUserPath()
    reData = {'src':[]}
    Src = []
    for i in imgdict['imgdata']:
        # print(i)
        fepath = getuserpath.getuserserpath(LoginRes['useremail'], i['fepath'])
        # print(fepath)
        fesrc = GetImgConPath1(fepath)
        Src.append(fesrc)
    reData['src'] = Src
    # print(imgdict['imgdata'])
    return JsonResponse(reData)

@require_POST
def ReName(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    ReNameInfo = request.POST.dict()
    fileOper = FileOper.FileOper()
    # print(request.POST)

    getuserpath = GetUserPath.GetUserPath()
    userPath = getuserpath.getuserserpath(LoginRes['useremail'], ReNameInfo['OldNamePath'])
    res = fileOper.Rename(userPath ,ReNameInfo['NewName'])

    userfilerecordmanage = UserFileRecordManage.userfilerecordmanage()
    userfilerecordmanage.NewName(ReNameInfo['OldNamePath'],ReNameInfo['NewName'])
    return HttpResponse(res)


@require_POST
def netOper(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    netoper = FileOper.netOper()

    try:
        info = request.POST.dict()
        if 'netOper' not in info:
            info = json.loads(request.body)
    except:
        info = json.loads(request.body)
    res = netoper.netOperMain(LoginRes['useremail'],info)
    return HttpResponse(res)

@require_POST
def QuitLogin(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    # response = redirect('/login/')
    response = JsonResponse({'res':'ok'})
    response.delete_cookie('coks')
    return response

# @require_POST
# def FileDown(request):
#     # print(request.POST)
#     LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
#     if LoginRes['res']:
#         return HttpResponseRedirect('/login/')
#     if request.method == 'POST':
#         downinfo = request.POST['downinfo']
#     else:
#         downinfo = request.GET['downinfo']
#     getuserpath = GetUserPath.GetUserPath()
#     downinfo = getuserpath.GetDownPath(downinfo,LoginRes)
#     FileDowUpCOm = FileDownUp.FileDU()
#     res = FileDowUpCOm.Down(downinfo)
#     return res
#
# @require_POST
# def FileUp(request):
#     LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
#     if LoginRes['res']:
#         return HttpResponseRedirect('/login/')
#     # print(request.FILES.get("file"))
#     file_obj = request.FILES.get("file")
#     # print(file_obj)
#     with open('static/uptest/' + file_obj.name, "wb") as f:
#         for chunk in file_obj.chunks(chunk_size=2 * 1024 * 1024):
#             f.write(chunk)
#     return HttpResponse('1')

#os.symlink(src,dst)创建软链接
