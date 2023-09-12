# Create your models here.
from django.db import models
from django.contrib.auth.models import User
# import time
# from ROOT.common.storage import OverwriteStorage
from django.contrib.auth.models import User
class Adpages(models.Model):
    adpage_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=225)
    action_name = models.CharField(max_length=225)
    controller_name = models.CharField(max_length=225)

    class Meta:
        managed = True
        db_table = 'adpages'
class UsersTable(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    forgot_password_token = models.CharField(max_length=100,null = True)
    email_token = models.CharField(max_length=200,null=True)
    isVerified= models.BooleanField(default=False)
    isAdmin = models.BooleanField(default=False)

    

    class Meta:
        managed = True
        db_table = 'users_table'