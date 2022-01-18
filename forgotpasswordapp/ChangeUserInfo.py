from Usersapp.models import User
from django.contrib.auth import authenticate,login,logout

class ChangeUserfo():
    def __init__(self):
        pass

    def CheckUser(self,email):
        if User.objects.filter(email=email).exists():
            return 1
        return 0

    def ChangePassword(self,email,password):
        if User.objects.filter(email=email).exists():
            Userfo = User.objects.get(email=email)
            Userfo.set_password(password)
            Userfo.save()
            return 1
        else:
            return 0