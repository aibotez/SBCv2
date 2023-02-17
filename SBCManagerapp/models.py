from django.db import models

# Create your models here.
class SBCManager(models.Model):
    FileStock = models.CharField(max_length=256)
    UserStock = models.CharField(max_length=256)
    SBCStockSize = models.IntegerField()
    SBCUser0 = models.CharField(max_length=20)
    SBCUserPass0 = models.CharField(max_length=20)
    SBCManageEmail = models.CharField(max_length=30)
    par1 = models.CharField(max_length=256)
    par2 = models.CharField(max_length=256)
    par3 = models.CharField(max_length=256)