from django.shortcuts import render, redirect
from .models import *
from Company.models import *
from Employees.models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .utils import *
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
from django.contrib.auth.models import User


def home(request):
    temp_dict = {}
    return render(request, 'SuperPanel/home_page.html', temp_dict)


def loginUser(request):
    if(request.body):
        data = json.loads(request.body)
        print(data)
        objs = User.objects.filter(email = data['email'])
        if(objs.count() > 0):
            user = authenticate(username = objs[0].username, password = data['password'])
            print(user)
            if user is not None:
                login(request, user)
                print("successfully logged in user")
                # send_mail_common("New User", "You Have Successfully LoggedIn", "", "noobda44@gmail.com", [objs[0].email])
                return JsonResponse({"status": "success", "message": "User LoggedIn Successfully"})
            else:
                return JsonResponse({"status": "error"})
        else:
            return JsonResponse({"status": "error", "message": "No Such User Exists"})
    temp_dict = {}
    return render(request, 'SuperPanel/signIn.html', temp_dict)


def signup(request):
    if(request.body):
        data = json.loads(request.body)
        print(data)
        user = User.objects.filter(username=data['email'])
        if user.count() == 0:
            user = create_user(data['name'], data['email'], data['password'], "COMMON_EMPLOYEE")
            print(user)
            if user is not None:
                login(request, user)
                send_mail_common("New User", "You Have Successfully SignedUp. Password Is: "+data['password'], "", "noobda44@gmail.com", [data['email']])
                return JsonResponse({"status": "success", "message": "User Created Successfully"})
        else:
            return JsonResponse({"status": "error", "message": "User Email Already Exists"})
    temp_dict = {}
    return render(request, 'SuperPanel/signUp.html', temp_dict)


def logoutMe(request):
    logout(request)
    return HttpResponseRedirect("/superpanel/login")


def forgotpass(request):
    if(request.body):
        data = json.loads(request.body)
        print(data)
        obj = User.objects.filter(email = data['email'])
        if(obj.count() > 0):
            obj = UserExtention.objects.get(user__email = data['email'])
            obj.resetToken = create_new_resetPassword_token()
            obj.save()
            link = settings.SERVER_BASE_URL + "/superpanel/getLink?username="+obj.user.username+"&resetToken="+obj.resetToken
            send_mail_common("Password Reset Link", "Here is Your Password Reset Link. Link : " + link, "", "noobda44@gmail.com", [data['email']])
            print("done", link)
            return JsonResponse({"status": "success", "message": "Reset Email Sent Successfully"})
        else:
            return JsonResponse({"status": "error", "message": "User Email Doesn't Exist"})
    temp_dict = {}
    return render(request, 'SuperPanel/forgotPassword.html', temp_dict)


def getLink(request):
    obj = UserExtention.objects.filter(user__username = request.GET['username'], resetToken = request.GET['resetToken'])
    if(obj.count() > 0):
        obj = obj[0]
        if(request.body):
            data = json.loads(request.body)
            obj.password = data['password']
            obj.resetToken = ""
            obj.save()
            print(obj.password)
            obj = obj.user
            obj.password = make_password(data['password'])
            obj.save()
            return JsonResponse({"status": "success", "message": "Password Reset Successfully"})
        temp_dict = {}
        temp_dict['user'] = obj
        temp_dict['link'] = "?username="+obj.user.username+"&resetToken="+obj.resetToken
        return render(request, 'SuperPanel/resetPassword.html', temp_dict)
    else:
        return JsonResponse({"status": "error", "message": "Incorrect Access"})


@login_required
def view_company(request):
    if(user_type(request, ["SUPER_ADMIN"])):
        search = 0
        if(request.GET):
            my_list = []
            if(request.GET.get('c_type') and request.GET['c_type'] != ""):
                search = 1
                my_list.append(Q(company_type = request.GET['c_type']))

            if(request.GET.get('c_name') and request.GET['c_name'] != ""):
                search = 1
                my_list.append(Q(name__icontains = request.GET['c_name']))

            if(request.GET.get('c_status') and request.GET['c_status'] != ""):
                search = 1
                my_list.append(Q(company_status = request.GET['c_status']))

        if(search == 1):
            data = Company.objects.filter(reduce(operator.and_, my_list))
        else:
            data = Company.objects.all()

        temp_dict = {}
        temp_dict['companies'] = data

        return render(request, 'SuperPanel/view_company.html', temp_dict)
    return JsonResponse({'status': "ERROR", 'message': "NOT ALLOWED TO ACCESS THIS PAGE"})


@login_required
def edit_company(request):
    if(user_type(request, ["SUPER_ADMIN"])):
        obj = None
        if(request.GET.get('id')):
            obj = Company.objects.filter(pk = request.GET['id'])
            if(obj.count() > 0):
                obj = obj[0]
                if(request.POST):
                    data = request.POST
                    if(User.objects.filter(email = data['hr_email']).count() == 0):
                        print(request.FILES)
                        obj = User()
                        obj.username = data['hr_email']
                        obj.email = data['hr_email']
                        obj.password = make_password(data['hr_password'])
                        obj.save()

                        obj1 = UserExtention()
                        obj1.type = data['user_type']
                        obj1.user = obj
                        obj1.mobile = data['c_person_phone']
                        obj1.password = data['hr_password']
                        obj1.save()

                        obj = Company()
                        obj.company_admin_user = obj1
                        obj.name = data['c_name']
                        obj.contact_person_name = data['c_person_name']
                        obj.contact_person_email = data['c_person_email']
                        obj.website = data['c_web']
                        if('c_logo' in request.FILES):
                            obj.logo = request.FILES['c_logo']
                        obj.address = data['c_address']
                        obj.email_address = data['c_email']
                        obj.company_type = data['c_type']
                        obj.company_status = data['c_status']
                        if(data['c_status'] == "ACTIVE"):
                            obj.is_company_active = True
                        else:
                            obj.is_company_active = False
                        obj.save()
                    else:
                        return JsonResponse({'status': "ERROR", "message": "USER WITH EMAIL ID " + data['hr_email'] +" ALREADY EXISTS !!"})
            else:
                return JsonResponse({'status': "ERROR", 'message': "NO SUCH COMPANY EXISTS"})

        temp_dict = {}
        temp_dict['company'] = obj
        return render(request, 'SuperPanel/edit_company.html', temp_dict)

    return JsonResponse({'status': "ERROR", 'message': "NOT ALLOWED TO ACCESS THIS PAGE"})


@login_required
def create_company(request):
    if(user_type(request, ["SUPER_ADMIN"])):
        temp_dict = {}
        return render(request, 'SuperPanel/create_company.html', temp_dict)
    else:
        return JsonResponse({'status': "ERROR", 'message': "NOT ALLOWED TO ACCESS THIS PAGE"})


@login_required
def save_company(request):
    if(user_type(request, ["SUPER_ADMIN"])):

        data = request.POST
        status = "ERROR"
        if(User.objects.filter(email = data['hr_email']).count() == 0):
            print(request.FILES)
            obj = User()
            obj.username = data['hr_email']
            obj.email = data['hr_email']
            obj.password = make_password(data['hr_password'])
            obj.save()

            obj1 = UserExtention()
            obj1.type = data['user_type']
            obj1.user = obj
            obj1.mobile = data['c_person_phone']
            obj1.password = data['hr_password']
            obj1.save()

            obj = Company()
            obj.company_admin_user = obj1
            obj.name = data['c_name']
            obj.contact_person_name = data['c_person_name']
            obj.contact_person_email = data['c_person_email']
            obj.website = data['c_web']
            if('c_logo' in request.FILES):
                obj.logo = request.FILES['c_logo']
            obj.address = data['c_address']
            obj.email_address = data['c_email']
            obj.company_type = data['c_type']
            obj.company_status = data['c_status']
            if(data['c_status'] == "ACTIVE"):
                obj.is_company_active = True
            else:
                obj.is_company_active = False
            obj.save()
            status = "SUCCESS"
            return JsonResponse({'status': status})
        else:
            return JsonResponse({'status': "ERROR", "message": "USER WITH EMAIL ID " + data['hr_email'] +" ALREADY EXISTS !!"})
    else:
        return JsonResponse({'status': "ERROR", 'message': "NOT ALLOWED TO ACCESS THIS PAGE"})


@login_required
def change_company_status(request, id):
    if(user_type(request, ["SUPER_ADMIN"])):
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


def convert_xls(worksheet, offset=0):
    rows = []
    print
    worksheet.nrows, worksheet.ncols
    for i, row in enumerate(range(worksheet.nrows)):
        if i <= offset:
            continue
        r = []
        for j, col in enumerate(range(worksheet.ncols)):
            r.append(worksheet.cell_value(i, j))
        rows.append(r)
    return rows


def upload_sheet(id):
    file = UploadData.objects.get(pk = id).file
    response = urllib.request.urlopen(settings.SERVER_BASE_URL + settings.MEDIA_URL + file.name)
    workbook = xlrd.open_workbook(file_contents = response.read())
    worksheet = workbook.sheet_by_index(0)
    rows = convert_xls(worksheet, 0)
    blank = 0
    count = 0
    for row in rows:
        data = create_employee_dict(UploadData.objects.get(pk = id).c_logo, row)
        create_save_employee(id, data)
    return True


@login_required
def bulk_upload(request):
    if(user_type(request, ["SUPER_ADMIN"])):
        temp_dict = {}
        temp_dict['companies'] = Company.objects.all()
        return render(request, 'SuperPanel/bulk_upload_view.html', temp_dict)
    return JsonResponse({'status': "ERROR", 'message': "NOT ALLOWED TO ACCESS THIS PAGE"})


@login_required
def save_upload(request):
    if(user_type(request, ["SUPER_ADMIN"])):
        if(request.POST):
            company = Company.objects.get(pk = request.POST['c_name'])
            obj = UploadData()
            obj.company = company
            try:
                obj.c_logo = request.FILES['c_logo']
            except:
                pass
            try:
                obj.file = request.FILES['sheet']
            except:
                pass
            obj.save()
            upload_sheet(obj.id)
            return JsonResponse({'status': "SUCCESS", "id": obj.id})

    return JsonResponse({'status': "ERROR", 'message': "NOT ALLOWED TO ACCESS THIS PAGE"})


@login_required
def bulk_upload_status(request):
    if(user_type(request, ["SUPER_ADMIN"])):
        obj = None
        if(request.GET.get('id')):
            obj = UploadData.objects.filter(pk = request.GET['id'])
            if(obj.count() > 0):
                obj = obj[0]
        temp_dict = {}
        temp_dict['data'] = obj
        return render(request, 'SuperPanel/bulk_upload.html', temp_dict)
    return JsonResponse({'status': "ERROR", 'message': "NOT ALLOWED TO ACCESS THIS PAGE"})


@login_required
def super_admin_login(request):
    search = 0
    my_list = []
    if(user_type(request, ["SUPER_ADMIN", "COMPANY_ADMIN"])):
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

            if(request.GET.get('p_url') and request.GET['p_url'] != ""):
                search = 1
                print(type(request.GET['p_url']))
                print(str_bool(request.GET['p_url']))
                my_list.append(Q(is_profile_link_active = str_bool(request.GET['p_url'])))

            if(user_type(request, ["SUPER_ADMIN"]) and request.GET.get('c_name') and request.GET['c_name'] != ""):
                search = 1
                my_list.append(Q(company = Company.objects.get(id = request.GET['c_name'])))

        if(search == 1):
            data = Employee.objects.filter(reduce(operator.and_, my_list))
        else:
            data = Employee.objects.all()

        temp_dict = {}
        if(user_type(request, ["COMPANY_ADMIN"])):
            temp_dict['type'] = "COMPANY_ADMIN"
            data = Employee.objects.filter(company__company_admin_user__user = request.user)
        else:
            temp_dict['type'] = "SUPER_ADMIN"
        temp_dict['employees'] = data
        temp_dict['employees_id'] = list(data.values_list('pk', flat = True))
        # print(list(data.values_list('pk', flat = True)))
        temp_dict['companies'] = Company.objects.all()
        return render(request, 'SuperPanel/company_user.html', temp_dict)

    return JsonResponse({'status': "ERROR", 'message': "NOT ALLOWED TO ACCESS THIS PAGE"})


@login_required
def change_employee_status(request, id):
    if(user_type(request, ["SUPER_ADMIN"])):
        status = "ERROR"
        obj = Employee.objects.filter(pk = id)
        if(obj.count() > 0):
            obj = obj[0]
            data = json.loads(request.body)
            print(data)
            if('profile_link' in data):
                stat = data['profile_link']
                obj.is_profile_link_active = str_bool(data['profile_link'])
            elif('edit_status' in data):
                stat = data['edit_status']
                obj.is_profile_editing_active = str_bool(data['edit_status'])
            elif('profile_status' in data):
                stat = data['profile_status']
                obj.is_profile_status_active = str_bool(data['profile_status'])
            else:
                pass
            obj.save()
            status = "SUCCESS"
            return JsonResponse({'status': status, 'current_status': stat})
    return JsonResponse({'status': "ERROR", 'message': "NOT ALLOWED TO ACCESS THIS PAGE"})


@login_required
def send_credentails(request, pk):
    if(user_type(request, ["SUPER_ADMIN"])):
        try:
            obj = Employee.objects.get(pk = pk)
            send_mail_common("USER CREDENTIALS FOR MY CARDS", "Here is your credentials for Your My Cards Account. Username : "+ obj.user.user.username +" Password : "+ obj.user.password +" Email Address : "+obj.user.user.email, "", "noobda44@gmail.com", [obj.user.user.email])
            return JsonResponse({'status': "SUCCESS"})
        except Exception as e:
            print(e)
            return JsonResponse({'status': "ERROR"})
    return JsonResponse({'status': "ERROR", 'message': "NOT ALLOWED TO ACCESS THIS PAGE"})


@login_required
def exportData(request):
    data = json.loads(request.body)
    print(data)
    return JsonResponse({'status': "SUCCESS"})
