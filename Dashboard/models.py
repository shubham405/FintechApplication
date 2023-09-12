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
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=150, null=True)
    password = models.CharField(max_length=300)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        managed = True
        db_table = 'users_table'