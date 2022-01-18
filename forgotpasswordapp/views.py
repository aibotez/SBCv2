from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from django.http import HttpResponse,JsonResponse
from LoginRegisterapp.LoginRegisterManage import registerOper,loginOper
from Vcodeapp import VcodeManage
from forgotpasswordapp import ChangeUserInfo

def forgotpassword(request):
    return render(request, 'forgotpass/forgot-password-v2.html')

@require_POST
def VerifyVcode(request):
    if request.method == 'POST':
        Vcode = request.POST['Vcode']
        useremail = request.POST['useremail']

        changeuserInfo = ChangeUserInfo.ChangeUserfo()
        msg = changeuserInfo.CheckUser(useremail)
        if msg:
            vcodemanage = VcodeManage.VcodeManage()
            msg='验证码错误'
            VerRes = vcodemanage.VerifyVcode(useremail,Vcode)
            if VerRes:
                msg = ''
                return render(request, 'forgotpass/recover-password-v2.html',locals())
            return render(request, 'forgotpass/forgot-password-v2.html',locals())
        msg = '用户不存在'
        return render(request, 'forgotpass/forgot-password-v2.html', locals())

@require_POST
def ChangePassword(request):
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        useremail = request.POST['useremail']

        msg=''
        if password1 != password2:
            msg = '两次密码不一致'
            return render(request, 'forgotpass/recover-password-v2.html', locals())
        if password1 == '':
            msg = '密码不能为空'
            return render(request, 'forgotpass/recover-password-v2.html', locals())
        else:
            changeuserInfo = ChangeUserInfo.ChangeUserfo()
            msg = changeuserInfo.ChangePassword(useremail,password1)
            if msg:
                return render(request, 'home/home.html')
            msg = '未知错误'
            return render(request, 'forgotpass/recover-password-v2.html', locals())
