from django.shortcuts import render
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from SBC import LoginVerfiy
from django.http import HttpResponseRedirect
from django.http import HttpResponse,JsonResponse
import json
from UserFileRecordapp import models
from django.db.models import Q

# Create your views here.


from django.core import serializers
@require_POST
def SBCSearchFile(request):
    LoginRes = LoginVerfiy.LoginVerfiy().verifylogin(request)
    if LoginRes['res']:
        return HttpResponseRedirect('/login/')


    SearchInfo = json.loads(request.body)
    print(SearchInfo)
    SearchContent = SearchInfo['SearchContent']
    SearchFileType = SearchInfo['SearchFileType']

    if SearchContent =='':
        SearchResult = models.UserFileRecord.objects.filter(Q(useremail = LoginRes['useremail']) & Q(FileType = SearchFileType))
        if SearchResult.exists():
            # SearchResult = models.UserFileRecord.objects.get(Q(useremail = LoginRes['useremail']) & Q(FileType = SearchFileType))
            for i in SearchResult:
                print(i.FilePath)
        return JsonResponse({'error':'0','data':serializers.serialize("json", SearchResult)})
