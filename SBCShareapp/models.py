from django.db import models

# Create your models here.

class SBCShare(models.Model):
    ShareLink = models.CharField(max_length=32)
    ShareFileInfo = models.CharField(max_length=500)
    useremail = models.CharField(max_length=32)
    password = models.CharField(max_length=20)
    ShareTime = models.IntegerField()
    # ShareTimeLimited = models.CharField(max_length=14)
    toUser = models.CharField(max_length=32)

