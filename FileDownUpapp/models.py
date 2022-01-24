from django.db import models

# Create your models here.

class FilesStock(models.Model):
    FileMd5 = models.CharField(max_length=256)
    FilePath = models.CharField(max_length=256)
    FileName = models.CharField(max_length=256)
