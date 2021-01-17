from django.shortcuts import render, redirect
from .models import *
from Company.models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from SuperPanel.utils import *
from Employees.models import *
import json
from functools import reduce
import operator
from io import BytesIO
import xlwt
import csv
import xlrd
import xlsxwriter
import urllib.request
from django.conf import settings
from django.contrib.auth import logout


@login_required
def company_users(request):
    if(user_type(request, ["SUPER_ADMIN", "COMPANY_ADMIN"])):
        search = 0
        my_list = []
        if(request.GET):
            if(request.GET.get('name') and request.GET['name'] != ""):
                search = 1
                my_list.append(Q(user__user__first_name__icontains = request.GET['name']))

            if(request.GET.get('email') and request.GET['email'] != ""):
                search = 1
                my_list.append(Q(user__user__email = request.GET['email']))

            if(request.GET.get('phone') and request.GET['phone'] != ""):
                search = 1
                my_list.append(Q(user__mobile__icontains = request.GET['phone']))

            if(request.GET.get('p_status') and request.GET['p_status'] != ""):
                search = 1
                my_list.append(Q(is_profile_status_active = str_bool(request.GET['p_status'])))

            if(request.GET.get('is_edit') and request.GET['is_edit'] != ""):
                search = 1
                my_list.append(Q(is_profile_editing_active = str_bool(request.GET['is_edit'])))

            if(request.GET.get('user_id') and request.GET['user_id'] != ""):
                search = 1
                my_list.append(Q(user__user__username = request.GET['user_id']))

        if(search == 1):
            data = Employee.objects.filter(reduce(operator.and_, my_list))
        else:
            data = Employee.objects.all()

        temp_dict = {}
        temp_dict['employees'] = data
        temp_dict['employees_id'] = list(data.values_list('pk', flat = True))
        return render(request, 'Company/company_admin_login.html', temp_dict)

    return JsonResponse({'status': "ERROR", 'message': "NOT ALLOWED TO ACCESS THIS PAGE"})


@login_required
def change_company_status(request, id):
    if(user_type(request, ["SUPER_ADMIN", "COMPANY_ADMIN"])):
        status = "ERROR"
        data = json.loads(request.body)
        print(data)
        if('company_status' in data):
            obj = Company.objects.filter(id = id)
            if(obj.count() > 0):
                obj = obj[0]
                obj.company_status = data['company_status']
                obj.save()
                status = "SUCCESS"
        return JsonResponse({'status': status, 'current_company_status': data['company_status']})
    return JsonResponse({'status': "ERROR", 'message': "NOT ALLOWED TO ACCESS THIS PAGE"})
