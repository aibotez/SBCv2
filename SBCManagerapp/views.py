from django.shortcuts import render
from django.shortcuts import render
import os,hashlib
from django.contrib.auth.decorators import login_required
from SBC import LoginVerfiy
from django.http import HttpResponse,JsonResponse
from django.http import HttpResponseRedirect
# Create your views here.


def sbcmanger(request):
    return render(request, "SBCManager/sbcmanager.html", locals())