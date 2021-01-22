from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from .choices import *


class UserExtention(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    type = models.CharField(max_length = 100, choices = USER_TYPE_CHOICES, null = False)
    mobile = models.CharField(max_length = 30, null = True, blank = True)
    password = models.CharField(max_length=1000, blank=True, null = True)
    resetToken = models.CharField(max_length=1000, blank=True, null = True)


from Employees.models import *
from Company.models import *


class UploadData(models.Model):
    successful_count = models.IntegerField(default = 0)
    unsuccessful_count = models.IntegerField(default = 0)
    file = models.FileField(upload_to='employee_upload_file', blank=True)
    c_logo = models.FileField(upload_to='company_logos', blank=True)
    company = models.ForeignKey(Company, on_delete = models.CASCADE, null = True, blank = True)
    users_list = models.ManyToManyField(Employee, blank = True)
