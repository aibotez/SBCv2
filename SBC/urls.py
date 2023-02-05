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
from FileDownUpapp import views as viewDU
from SBCShareapp import views as viewShare
from previewapp import views as viewPre
from BaiduNetapp import views as viewBdn
from SBCFileSearch import views as viewSBCFS
from HomeManageapp import  views as viewHM
from Usersapp import views as viewUser
from FileSycapp import views as viewFS

urlpatterns = [
    path('', view.Home),
    path('ConnectTest/',view.ConnectTest),
    path('GetUserInfo/',viewUser.GetUserInfo),
    path('RefreshFiles/', view.FileList),
    path('DelFiles/',view.DelFiles),
    path('ReName/',view.ReName),
    path('netOper/',view.netOper),
    path('admin/', admin.site.urls),
    path('login/',viewsLR.login),
    path('register/',viewsLR.Register),
    path('home/',view.Home),
    path('GetImgCon/',view.GetImgCon),
    path('QuitLogin/',view.QuitLogin),
    path('GetFileListbyClient/',view.GetFileListbyClient),
    path('GetAllFilesfromFolder/',view.GetAllFilesfromFolder),
    path('GetFileMd5/',view.GetFileMd5),
    path('GetFilePorper/',view.GetFilePorper),

    path('GetAllFilesSyc/',viewFS.GetAllFilesfromFolder),
    path('SycCheckSBCFile/',viewFS.CheckSBCFile),

    path('FileDown/',viewDU.FileDown),
    path('FileDown1/',viewDU.FileDown1),

    path('Upfile/',viewDU.FileUp),
    path('Upfile1/',viewDU.FileUp1),
    path('CheckFile/',viewDU.CheckFile),
    path('GetVcode/',views.GetVcode),
    path('VerifyVcode/',views.VerifyVcode),
    path('registerVerify/',viewsLR.registerVerify),
    path('loginVerify/',viewsLR.loginVerify),

    path('forgotpassword/',viewFG.forgotpassword),
    path('forgotpassVcodeVerify/',viewFG.VerifyVcode1),
    path('ChangePassword/',viewFG.ChangePassword),


    path('CreatShareFile/',viewShare.CreatShareFile),
    path('SBCShare/',viewShare.SBCShareShow),
    path('GetSBCShareFile/',viewShare.GetSBCShareFile),
    path('ShareSave2SBC/',viewShare.ShareSave2SBC),

    path('preview/',viewPre.preview),

    path('BaiduNetUserExistCheck/',viewBdn.BaiduNetUserExistCheck),
    path('BaiduNetSaveUser/',viewBdn.BaiduNetSaveUser),
    path('BaiduNetShow/',viewBdn.BaiduNetShow),
    path('BaiduNetHome/',viewBdn.BaiduNetHome),
    path('GetBDDownLink/',viewBdn.GetBDDownLink),
    path('BaiduNetQuitLogin/',viewBdn.BaiduNetQuitLogin),
    path('reD/',viewBdn.reD),

    path('SearchFile/',viewSBCFS.SBCSearchFile),


    path('HM/',viewHM.TurnOnComputer),
]
