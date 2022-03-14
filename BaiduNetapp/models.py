from django.db import models

# Create your models here.
class BaiduNetUserManage(models.Model):
    useremail = models.CharField(max_length=32)
    cookie = models.CharField(max_length=500)

