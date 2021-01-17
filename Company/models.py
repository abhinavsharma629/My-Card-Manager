from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from .choices import *
from SuperPanel.models import UserExtention


class Company(models.Model):
    company_admin_user = models.ForeignKey(UserExtention, on_delete = models.CASCADE)
    name = models.CharField(max_length=1000)
    website = models.URLField(max_length=1000, blank=True, null = True)
    logo = models.FileField(upload_to='company_logos', blank=True)
    contact_person_name = models.CharField(max_length=1000, blank=True, null = True)
    contact_person_email = models.EmailField(max_length=1000, blank=True, null = True)
    addresss = models.TextField(blank=True, null = True)
    email_address = models.EmailField(max_length=1000, blank=True, null = True)
    company_type = models.CharField(max_length = 1000, choices = COMPANY_TYPES, null = False)
    company_status = models.CharField(max_length = 1000, choices = COMPANY_STATUS, null = False)
    is_company_active = models.BooleanField(default = False)
