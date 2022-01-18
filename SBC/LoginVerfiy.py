from django.shortcuts import render
from Usersapp.models import User
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

class LoginVerfiy():
    def __init__(self):
        self.FailureUrl = '/login.login.html'

    def verifylogin(self,request):
        cookies = request.COOKIES
        if 'coks' in cookies:
            usefo = cookies['coks'].split('auth:')
            if User.objects.get(email=usefo[0]).password == usefo[1]:
                return 0
        return 1

        # return render(request,self.FailureUrl)