from django.db import models

# Create your models here.

class UserFileRecord(models.Model):

    useremail = models.CharField(max_length=32)
    FileMd5 = models.CharField(max_length=100)
    FileType = models.CharField(max_length=10)
    FilePath = models.CharField(max_length=200)
    FileSize = models.IntegerField()
    FileModTime = models.CharField(max_length=100)
    Expansion = models.CharField(max_length=200)
