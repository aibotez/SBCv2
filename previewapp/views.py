
from SBC import FileType
from django.shortcuts import render
import os
from django.contrib.auth.decorators import login_required
from SBC import LoginVerfiy
from django.http import HttpResponse,JsonResponse
from django.http import HttpResponseRedirect
from SBC import GetUserPath
import base64,json
from previewapp import PreviewManager
# Create your views here.

def GetFeBase64(path):
    with open(path, 'rb') as f:
        # lsf = base64.b64decode(f.read())
        febase64 = base64.b64encode(f.read()).decode()
        # imgbase64Url = "data:image/{};base64,".format(imgtype) + imgbase64
        return febase64
def Convert2PDF(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    prep = json.loads(request.body)
    Previewmanager = PreviewManager.Preview()
    res = Previewmanager.Convert2pdf(LoginRes['useremail'],prep['path'])
    return HttpResponse(res)

def previewpdftest(path,page):
    import fitz
    from PyQt5.QtGui import QImage
    from PyQt5 import QtCore
    import base64
    # info = json.loads(request.body)
    # page = info['page']
    # path = 'static/TEMP/2290227486@qq.com/J-TEXT实验研究进展-陈忠勇.pptx.pdf'
    doc = fitz.open(path)
    pages = doc.page_count
    trans_a = 200
    trans_b = 200
    trans = fitz.Matrix(trans_a / 100, trans_b / 100).prerotate(0)
    pix = doc[page].get_pixmap(matrix=trans)
    fmt = QImage.Format_RGBA8888 if pix.alpha else QImage.Format_RGB888
    pageImage = QImage(pix.samples, pix.width, pix.height, pix.stride, fmt)
    data = QtCore.QByteArray()
    buf = QtCore.QBuffer(data)
    pageImage.save(buf, 'PNG')
    febase64 = base64.b64encode(data).decode()
    return {'pages':pages,data:febase64}
    # return HttpResponse(febase64, content_type="image/png")
    # return HttpResponse(febase64)


def preview(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    getuserpath = GetUserPath.GetUserPath()

    if request.method == 'GET':
        if 'client' in request.GET:
            req = {'path':request.GET['filepath'],'client':'','page':request.GET['page']}
        else:
            req = {'path': request.GET['filepath']}
    else:
        prep = json.loads(request.body)
        # print(json.loads(request.body),type(json.loads(request.body)))
        if 'client' in prep:
            req = {'path': prep['filepath'],'client':'','page':prep['page']}
        else:
            req = {'path': prep['filepath']}
    path = getuserpath.userpath(req,LoginRes)[1]
    FiletypeJudge = FileType.FileType()
    filetype = FiletypeJudge.GetFileType(path)[0]
    if filetype == 'image':

        image_data = open(path, "rb").read()

        return HttpResponse(image_data, content_type="image/png")
    elif filetype == 'pdf':
        if 'client' in req:
            # pdfbase64 = GetFeBase64(path)
            pdfbase64 = previewpdftest(path,req['page'])
            return JsonResponse({'data':pdfbase64})
        else:
        # pdfbase64 = "data:application/pdf;base64," + GetFeBase64(path)
            pdfbase64 = GetFeBase64(path)
        # return HttpResponseRedirect('/pdfviewer.html')
            return render(request, "preview/pdfviewer.html",locals())
    elif filetype == 'word' or filetype == 'ppt' or filetype =='excel' or filetype == 'html':
        FileName = os.path.basename(path)
        SerTempPath = 'static/TEMP/{}/{}.pdf'.format(LoginRes['useremail'],FileName)
        if not os.path.exists(SerTempPath):
            Previewmanager = PreviewManager.Preview()
            res = Previewmanager.Convert2pdf(LoginRes['useremail'], req['path'])

        if 'client' in req:
            pdfbase64 = previewpdftest(SerTempPath, req['page'])
            return JsonResponse({'data':pdfbase64})
        else:
            pdfbase64 = GetFeBase64(SerTempPath)
            return render(request, "preview/pdfviewer.html", locals())

def preview1(request):
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
