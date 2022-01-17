from django.shortcuts import render
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from django.http import HttpResponse,JsonResponse
from LoginRegisterapp.LoginRegisterManage import registerOper

# Create your views here.


def login(request):
    return render(request, "login/login.html")

@require_POST
def loginVerify(request):
    pass

def Register(request):
    return render(request, "register/register_v2.html")

@require_POST
def registerVerify(request):
    userinfo = request.META
    if 'HTTP_X_FORWARDED_FOR' in userinfo.keys():
        useripv4 = request.META['HTTP_X_FORWARDED_FOR']
    else:
        useripv4 = request.META['REMOTE_ADDR']
    if request.method == 'POST':
        request.POST = request.POST.copy()
        userInfos = request.POST
        username = userInfos['username']
        userpassword = userInfos['userpassword1']
        useremail = userInfos['useremail']
        vcode = userInfos['vcode']
        userInfos['ipv4'] = useripv4
        Reg = registerOper()
        info = Reg.registeract(userInfos)
        if info == 1:
            return HttpResponse('ok')
        return HttpResponse(info)