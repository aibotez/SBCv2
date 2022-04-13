from django.db import models

# Create your models here.

class UserFileRecord(models.Model):

    useremail = models.CharField(max_length=32)
    FileType = models.CharField(max_length=10)
    FilePath = models.CharField(max_length=200)
