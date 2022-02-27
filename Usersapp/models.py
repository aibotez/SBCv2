from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    tel = models.CharField(max_length=11, unique=False, verbose_name='手机号')
    ipv4 = models.CharField(max_length=32)
    usedcapacity = models.IntegerField()
    totalcapacity = models.IntegerField()