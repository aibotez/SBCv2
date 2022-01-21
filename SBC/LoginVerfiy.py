from django.shortcuts import render
from Usersapp.models import User
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

class LoginVerfiy():
    def __init__(self):
        self.FailureUrl = '/login.login.html'

    def verifylogin(self,request):
        cookies = request.COOKIES
        LoginRes = {'res':1,'useremail':''}
        if 'coks' in cookies:
            usefo = cookies['coks'].split('auth:')
            if User.objects.filter(email=usefo[0]).exists():
                if User.objects.get(email=usefo[0]).password == usefo[1]:
                    LoginRes['res'] = 0
                    LoginRes['useremail'] = usefo[0]
                    return LoginRes
        return LoginRes

        # return render(request,self.FailureUrl)