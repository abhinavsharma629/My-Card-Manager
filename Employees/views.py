from django.shortcuts import render, redirect
from .models import *
from Company.models import *
from SuperPanel.models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from functools import reduce
from SuperPanel.utils import *
import operator
from io import BytesIO
import xlwt
import csv
import xlrd
import xlsxwriter
import urllib.request
from django.conf import settings
from django.contrib.auth import logout
from .utils import *


@login_required
def edit_profile(request):
    if(user_type(request, ["SUPER_ADMIN", "COMPANY_ADMIN", "COMPANY_EMPLOYEE", "COMMON_EMPLOYEE"])):
        obj = Employee.objects.filter(user__user__username = request.user.username)
        if(obj.count() > 0):
            temp_dict = {}
            # if(obj[0].is_profile_editing_active == False):
            #     return JsonResponse({'status': "ERROR", 'message': "YOU ARE NOT ALLOWED TO EDIT YOUR PROFILE"})
            if(request.POST):
                print(request.POST)
                print(updateEmployeeProfile(obj[0], request))
                return HttpResponseRedirect("/employees/edit-profile")
            
            temp_dict['obj'] = obj[0]
            return render(request, 'Employees/edit_profile.html', temp_dict)
        else:
            return JsonResponse({'status': "ERROR", 'message': "NO SUCH USER EXISTS IN OUR DATABASE"})
    return JsonResponse({'status': "ERROR", 'message': "NOT ALLOWED TO ACCESS THIS PAGE"})


def view_profile(request):
    print(settings.MEDIA_ROOT)
    if("username" in request.GET):
        obj = Employee.objects.filter(user__user__username = request.GET['username'])
        if(obj.count() > 0):
            temp_dict = {}
            temp_dict['obj'] = obj[0]
            return render(request, 'Employees/download_profile.html', temp_dict)

    return JsonResponse({'status': "ERROR", 'message': "NO SUCH USER EXISTS IN OUR DATABASE"})


def create_vcf(request):
    if("username" in request.GET):
        obj = Employee.objects.filter(user__user__username = request.GET['username'])
        if(obj.count() > 0):
            file = vcf_card(obj[0])
            try:
                with open("./%s" % obj[0].user.user.username + ".vcf", 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type='text/x-vcard')
                    response['Content-Disposition'] = 'inline; filename=' + obj[0].user.user.username + ".vcf"
                    return response
            except Exception as e:
                print(e)
                return JsonResponse({'status': "ERROR", 'message': "SOME ERROR OCCURED"})
    return JsonResponse({'status': "ERROR", 'message': "NO SUCH USER EXISTS IN OUR DATABASE"})
