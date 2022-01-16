from django.db import models

# Create your models here.
class Vcodemode(models.Model):
    useremail = models.CharField(max_length=32)
    Vcode = models.CharField(max_length=4)
    ipv4 = models.CharField(max_length=32)
    ipv6 = models.CharField(max_length=200)
    islocked = models.IntegerField()
    locklevel = models.IntegerField()
    firstrequesttime = models.IntegerField()
    lastrequesttime = models.IntegerField()
    retimesper = models.IntegerField()