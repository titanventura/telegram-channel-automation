from django.db import models
from django.contrib.auth.models import User
import datetime

class UserRecord(models.Model):

    def __str__(self):
        return self.name + ' ' + self.rollno

    user = models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=120,blank=False,null=False)
    rollno = models.CharField(max_length=10,unique=True)
    phone = models.CharField(max_length=10,unique=True)
    email = models.EmailField(max_length=50,unique=True)
    telegram_number = models.CharField(max_length=13,unique=True,blank=True,null=True)
    is_added_to_group = models.BooleanField(default=False)
    reason_for_error =  models.CharField(max_length=200,default="",blank=True)
    time_registered = models.DateTimeField(blank=True,default=datetime.datetime.min,null=True)
    time_added_to_group = models.DateTimeField(blank=True,default=datetime.datetime.min,null=True)