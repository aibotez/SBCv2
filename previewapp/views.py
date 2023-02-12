
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

def previewpdftest(request):
    import fitz
    from PyQt5.QtGui import QImage
    from PyQt5 import QtCore
    import base64
    info = json.loads(request.body)
    page = info['page']
    path = 'static/TEMP/2290227486@qq.com/J-TEXT实验研究进展-陈忠勇.pptx.pdf'
    doc = fitz.open(path)
    trans_a = 200
    trans_b = 200
    trans = fitz.Matrix(trans_a / 100, trans_b / 100).prerotate(0)
    pix = doc[page].get_pixmap(matrix=trans)
    fmt = QImage.Format_RGBA8888 if pix.alpha else QImage.Format_RGB888
    pageImage = QImage(pix.samples, pix.width, pix.height, pix.stride, fmt)

    data = QtCore.QByteArray()
    buf = QtCore.QBuffer(data)
    pageImage.save(buf, 'PNG')
    # str = data.toBase64()
    febase64 = base64.b64encode(data).decode()
    return HttpResponse(febase64, content_type="image/png")
    # return HttpResponse(febase64)


def previewpdftest1(request):

    # info = json.loads(request.body)
    # page = info['page']


    from django.http import StreamingHttpResponse, FileResponse
    from django.utils.encoding import escape_uri_path
    import fitz
    from PyQt5.QtGui import QImage
    from PyQt5 import QtCore
    import base64
    def file_iterator(file_name, chunk_size=20 * 1024 * 1024):
        doc = fitz.open(file_name)
        pages = doc.page_count
        print(pages)
        for i in range(pages):
            print(i)
            trans_a = 200
            trans_b = 200
            trans = fitz.Matrix(trans_a / 100, trans_b / 100).prerotate(0)
            pix = doc[i].get_pixmap(matrix=trans)
            fmt = QImage.Format_RGBA8888 if pix.alpha else QImage.Format_RGB888
            pageImage = QImage(pix.samples, pix.width, pix.height, pix.stride, fmt)

            data = QtCore.QByteArray()
            buf = QtCore.QBuffer(data)
            pageImage.save(buf, 'PNG')
            # str = data.toBase64()
            febase64 = base64.b64encode(data).decode()
            # print(66,data)
            # print(77,str)
            yield febase64
        # with open(file_name, 'rb') as f:
        #     while True:
        #         c = f.read(chunk_size)
        #         if c:
        #             febase64 = base64.b64encode(c).decode()
        #             yield febase64
        #         else:
        #             break
    path = 'static/TEMP/2290227486@qq.com/J-TEXT实验研究进展-陈忠勇.pptx.pdf'
    the_file_name = 'J-TEXT实验研究进展-陈忠勇.pptx.pdf'
    the_file_path = path
    # print(the_file_name,the_file_path)
    # response = FileResponse(file_iterator(the_file_name))
    response = StreamingHttpResponse(file_iterator(the_file_path))
    response = FileResponse(response)
    response['Content-Type'] = 'application/octet-stream'
    response['content-length'] = os.path.getsize(the_file_path)
    # response['Content-Disposition'] = 'attachment;filename="{0}"'.format(wjname)
    response["Content-Disposition"] = "attachment; filename*=UTF-8''{}".format(escape_uri_path(the_file_name))
    return response


def preview(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')
    getuserpath = GetUserPath.GetUserPath()

    if request.method == 'GET':
        if 'client' in request.GET:
            req = {'path':request.GET['filepath'],'client':''}
        else:
            req = {'path': request.GET['filepath']}
    else:
        prep = json.loads(request.body)
        # print(json.loads(request.body),type(json.loads(request.body)))
        if 'client' in prep:
            req = {'path': prep['filepath'],'client':''}
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
            pdfbase64 = GetFeBase64(path)
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
        pdfbase64 = GetFeBase64(SerTempPath)
        if 'client' in req:
            return JsonResponse({'data':pdfbase64})
        else:
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
