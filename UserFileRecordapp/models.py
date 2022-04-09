from django.db import models

# Create your models here.

class UserFileRecord(models.Model):

    useremail = models.CharField(max_length=32)
    password = models.CharField(max_length=20)
    ShareTime = models.IntegerField()
    # ShareTimeLimited = models.CharField(max_length=14)
    toUser = models.CharField(max_length=32)
