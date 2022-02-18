from django.db import models

# Create your models here.

class SBCShare(models.Model):
    ShareLink = models.CharField(max_length=32)
    ShareFilePath = models.CharField(max_length=100)
    useremail = models.CharField(max_length=32)
    password = models.CharField(max_length=10)
    ShareTime = models.CharField(max_length=14)
    ShareTimeLimited = models.CharField(max_length=14)
    toUser = models.CharField(max_length=32)

