from django.shortcuts import render
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from django.http import HttpResponse,JsonResponse
from LoginRegisterapp.LoginRegisterManage import registerOper,loginOper

# Create your views here.

def GrtIpv4(req):
    userinfo = req.META
    if 'HTTP_X_FORWARDED_FOR' in userinfo.keys():
        useripv4 = req.META['HTTP_X_FORWARDED_FOR']
    else:
        useripv4 = req.META['REMOTE_ADDR']
    return useripv4

def login(request):
    return render(request, "login/login.html")

@require_POST
def loginVerify(request):
    useripv4 = GrtIpv4(request)
    if request.method == 'POST':
        request.POST = request.POST.copy()
        userInfos = request.POST
        userInfos['ipv4'] = useripv4
        Login = loginOper()
        res = Login.LoginVerifyUser(userInfos)
        msg = '用户名或密码错误'
        if res:
            return HttpResponse('1')
        else:
            return render(request, "login/login.html",locals())


def Register(request):
    return render(request, "register/register_v2.html")

@require_POST
def registerVerify(request):
    useripv4 = GrtIpv4(request)
    if request.method == 'POST':
        request.POST = request.POST.copy()
        userInfos = request.POST
        userInfos['ipv4'] = useripv4
        Reg = registerOper()
        info = Reg.registeract(userInfos)
        if info == 1:
            return HttpResponse('ok')
        return HttpResponse(info)