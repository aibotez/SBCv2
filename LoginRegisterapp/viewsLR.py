from django.shortcuts import render

# Create your views here.


def login(request):
    return render(request, "login/login.html")

def Register(request):
    return render(request, "register/register_v2.html")