from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from SuperPanel.models import *
from Company.models import *


class PaymentDetail(models.Model):
    g_pay = models.CharField(max_length=1000, blank=True, default = "")
    apple_pay = models.CharField(max_length=1000, blank=True, default = "")
    paypal = models.CharField(max_length=1000, blank=True, default = "")
    samsung_pay = models.CharField(max_length=1000, blank=True, default = "")
    cash_app = models.CharField(max_length=1000, blank=True, default = "")


class ThirdPartConnection(models.Model):
    facebook = models.URLField(max_length=1000, blank=True, default = "")
    instagram = models.URLField(max_length=1000, blank=True, default = "")
    snapchat = models.URLField(max_length=1000, blank=True, default = "")
    linkedin = models.URLField(max_length=1000, blank=True, default = "")
    twitter = models.URLField(max_length=1000, blank=True, default = "")
    tumblr = models.URLField(max_length=1000, blank=True, default = "")
    dribble = models.URLField(max_length=1000, blank=True, default = "")
    behance = models.URLField(max_length=1000, blank=True, default = "")
    pinterest = models.URLField(max_length=1000, blank=True, default = "")
    youtube = models.URLField(max_length=1000, blank=True, default = "")
    telegram = models.URLField(max_length=1000, blank=True, default = "")
    reddit = models.URLField(max_length=1000, blank=True, default = "")


class Employee(models.Model):
    user = models.OneToOneField(UserExtention, on_delete = models.CASCADE, primary_key = True)
    middle_name = models.CharField(max_length=1000, blank=True, default = "")
    profile_picture = models.FileField(upload_to='profile_pictures', blank=True, null = True)

    profession = models.CharField(max_length=1000, blank=True, default = "")
    description = models.TextField(blank=True, default = "")
    job_title = models.CharField(max_length=1000, blank=True, default = "")
    company = models.OneToOneField(Company, on_delete = models.CASCADE, blank=True, null = True)

    whatsapp_number = models.CharField(max_length=30, blank=True, default = "")
    telephone_number = models.CharField(max_length=30, blank=True, default = "")
    fax_number = models.CharField(max_length=30, blank=True, default = "")
    website = models.URLField(max_length=1000, blank=True, default = "")
    skype_id = models.CharField(max_length=1000, blank=True, default = "")

    third_party_connection_details = models.OneToOneField(ThirdPartConnection, on_delete = models.CASCADE, blank = True, null = True)

    address1 = models.CharField(max_length=1000, blank=True, default = "")
    address2 = models.CharField(max_length=1000, blank=True, default = "")
    city = models.CharField(max_length=1000, blank=True, default = "")
    state = models.CharField(max_length=1000, blank=True, default = "")
    zipcode = models.CharField(max_length=1000, blank=True, default = "")
    country = models.CharField(max_length=1000, blank=True, default = "")

    another_address1 = models.CharField(max_length=1000, blank=True, default = "")
    another_address2 = models.CharField(max_length=1000, blank=True, default = "")
    another_city = models.CharField(max_length=1000, blank=True, default = "")
    another_state = models.CharField(max_length=1000, blank=True, default = "")
    another_zipcode = models.CharField(max_length=1000, blank=True, default = "")
    another_country = models.CharField(max_length=1000, blank=True, default = "")

    payment_details = models.OneToOneField(PaymentDetail, on_delete = models.CASCADE, blank = True, null = True)

    email_address1 = models.EmailField(max_length=1000, blank=True, default = "")
    email_address2 = models.EmailField(max_length=1000, blank=True, default = "")
    email_address3 = models.EmailField(max_length=1000, blank=True, default = "")
    website1 = models.URLField(max_length=1000, blank=True, default = "")
    website2 = models.URLField(max_length=1000, blank=True, default = "")
    website3 = models.URLField(max_length=1000, blank=True, default = "")
    mobile1 = models.CharField(max_length=30, blank=True, default = "")
    mobile2 = models.CharField(max_length=30, blank=True, default = "")
    mobile3 =  models.CharField(max_length=30, blank=True, default = "")

    profile_link = models.URLField(max_length=1000, blank=True, default = "")
    is_profile_link_active = models.BooleanField(default = False)
    is_profile_status_active = models.BooleanField(default = False)
    is_profile_editing_active = models.BooleanField(default = False)
