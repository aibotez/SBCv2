from django.shortcuts import render
from django.shortcuts import render
import os,hashlib
from django.contrib.auth.decorators import login_required
from SBC import LoginVerfiy
from django.http import HttpResponse,JsonResponse
from django.http import HttpResponseRedirect
from SBCManagerapp import models as SBCManagemodels
from UserFileRecordapp import models as UserFileRecordmodels
# Create your views here.
from Usersapp.models import User
from django.contrib.auth import authenticate,login,logout



def size_format(size):
    if size < 1024:
        return '%i' % size + 'B'
    elif 1024 <= size < 1024*1024:
        return '%.1f' % float(size/1024) + 'KB'
    elif 1024*1024 <= size < 1024*1024*1024:
        return '%.1f' % float(size/(1024*1024)) + 'MB'
    elif 1024*1024*1024 <= size < 1024*1024*1024*1024:
        return '%.1f' % float(size/(1024*1024*1024)) + 'GB'
    elif 1024*1024*1024*1024 <= size:
        return '%.1f' % float(size/(1024*1024*1024*1024)) + 'TB'

def sbcmanger(request):
    Users = User.objects.all()
    UserInfo = []
    j = 1
    for i in Users:
        userinfo = {}
        userinfo['username'] = i.username
        userinfo['id'] = i.id
        userinfo['numid'] = str(j)
        userinfo['usedcapacity'] = i.usedcapacity
        userinfo['totalcapacity'] = i.totalcapacity
        userinfo['is_superuser'] = i.is_superuser
        userinfo['usercapacityper'] = str(round((i.usedcapacity / i.totalcapacity) * 100,1))+'%'
        userinfo['usercapacityinfo'] = '{}/{}  ({})'.format(size_format(i.usedcapacity),size_format(i.totalcapacity),userinfo['usercapacityper'])

        UserInfo.append(userinfo)
        j += 1

    return render(request, "SBCManager/sbcmanager.html", locals())