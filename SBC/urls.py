"""SBC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import view
from Vcodeapp import views
from LoginRegisterapp import viewsLR
from forgotpasswordapp import views as viewFG

urlpatterns = [
    path('', view.Home),
    path('test/', view.home),
    path('admin/', admin.site.urls),
    path('login/',viewsLR.login),
    path('register/',viewsLR.Register),
    path('home/',view.Home),
    path('GetVcode/',views.GetVcode),
    path('VerifyVcode/',views.VerifyVcode),
    path('registerVerify/',viewsLR.registerVerify),
    path('loginVerify/',viewsLR.loginVerify),

    path('forgotpassword/',viewFG.forgotpassword),
    path('forgotpassVcodeVerify/',viewFG.VerifyVcode),
    path('ChangePassword/',viewFG.ChangePassword),
]
