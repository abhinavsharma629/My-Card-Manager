from .models import *
from Company.models import *
from Employees.models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import secrets
import string
from django.conf import settings
from django.core.mail import send_mail


def send_mail_common(subject, message, template, from_user, to):
    send_mail(
        subject,
        message,
        from_user,
        to,
        fail_silently = True,
    )
    return True


def create_unique_username():
    while(True):
        userId = str(secrets.token_urlsafe(10))
        if(User.objects.filter(username = userId).count() == 0):
            return userId


def create_user(name, email, password, type):
    try:
        obj = User()
        obj.first_name = name
        obj.email = email
        obj.username = create_unique_username()
        obj.password = make_password(password)
        obj.save()

        obj1 = UserExtention()
        obj1.user = obj
        obj1.type = type
        obj1.password = password
        obj1.save()

        if(type == "COMMON_EMPLOYEE" or type == "COMMON_EMPLOYEE"):
            obj2 = Employee()
            obj2.user = obj1
            obj2.save()
        return obj
    except Exception as e:
        print(e)
        return None


def user_type(request, users):
    obj = UserExtention.objects.filter(user = request.user)
    if(obj.count() > 0 and obj[0].type in users):
        return True
    return False


def create_password():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(8))  # for a 8-character password
    return password


def generate_profile_link(username):
    url = settings.SERVER_BASE_URL + "/employees/view_profile?username=" + username
    return url


def str_bool(data):
    if(data in ['true', 'True', '1']):
        return True
    return False


def create_third_party_connection_details(row):
    obj = ThirdPartConnection()
    obj.facebook = row[15]
    obj.instagram = row[41]
    obj.snapchat = row[42]
    obj.linkedin = row[43]
    obj.twitter = row[44]
    obj.tumblr = row[45]
    obj.dribble = row[46]
    obj.behance = row[47]
    obj.pinterest = row[48]
    obj.youtube = row[49]
    obj.telegram = row[50]
    obj.reddit = row[51]
    obj.save()
    return obj


def create_payment_details(row):
    obj = PaymentDetail()
    obj.g_pay = row[28]
    obj.apple_pay = row[52]
    obj.paypal = row[53]
    obj.samsung_pay = row[54]
    obj.cash_app = row[55]
    obj.save()
    return obj


def create_employee_dict(pic, row):
    data = {}

    data['email'] = row[0]
    data['first_name'] = row[1]
    data['last_name'] = row[2]
    data['mobile'] = row[3]

    data['middle_name'] = row[4]
    data['profile_picture'] = pic

    data['profession'] = row[6]
    data['description'] = row[7]
    data['job_title'] = row[8]
    data['company'] = Company.objects.get(pk = row[9])

    data['whatsapp_number'] = row[10]
    data['telephone_number'] = row[11]
    data['fax_number'] = row[12]
    data['website'] = row[13]
    data['skype_id'] = row[14]

    data['third_party_connection_details'] = create_third_party_connection_details(row)

    data['address1'] = row[16]
    data['address2'] = row[17]
    data['city'] = row[18]
    data['state'] = row[19]
    data['country'] = row[20]
    data['zipcode'] = row[21]

    data['another_address1'] = row[22]
    data['another_address2'] = row[23]
    data['another_city'] = row[24]
    data['another_state'] = row[25]
    data['another_zipcode'] = row[26]
    data['another_country'] = row[27]

    data['payment_details'] = create_payment_details(row)

    data['email_address1'] = row[29]
    data['email_address2'] = row[30]
    data['email_address3'] = row[31]
    data['website1'] = row[32]
    data['website2'] = row[33]
    data['website3'] = row[34]
    data['mobile1'] = row[35]
    data['mobile2'] = row[36]
    data['mobile3'] = row[37]

    data['is_profile_link_active'] = row[38]
    data['is_profile_status_active'] = row[39]
    data['is_profile_editing_active'] = row[40]

    return data


def create_save_employee(id, data):
    main_obj = UploadData.objects.get(pk = id)
    if(User.objects.filter(email = obj[0]).count() > 0):
        main_obj.unsuccessful_count += 1
        main_obj.save()
        return {"status": False, "message": "DUPLICATE"}
    else:
        # SAVE USER OBJECT
        password = make_password(create_password())
        username = create_unique_username()
        obj = User()
        obj.email = data['email']
        obj.username = username
        obj.password = password
        obj.first_name = data['first_name']
        obj.last_name = data['last_name']
        obj.save()

        # SAVE USEREXTENTION OBJECT
        obj1 = UserExtention()
        obj1.user = obj
        obj.type = "COMPANY_EMPLOYEE"
        obj1.mobile = data['mobile']
        obj1.password = password
        obj1.save()

        # SAVE EMPLOYEES OBJECT
        obj = Employee()
        obj.middle_name = data['middle_name']
        obj.profile_picture = data['profile_picture']

        obj.profession = data['profession']
        obj.description = data['description']
        obj.job_title = data['job_title']
        obj.company = data['company']

        obj.whatsapp_number = data['whatsapp_number']
        obj.telephone_number = data['telephone_number']
        obj.fax_number = data['fax_number']
        obj.website = data['website']
        obj.skype_id = data['skype_id']

        obj.third_party_connection_details = data['third_party_connection_details']

        obj.address1 = data['address1']
        obj.address2 = data['address2']
        obj.city = data['city']
        obj.state = data['state']
        obj.country = data['country']
        obj.zipcode = data['zipcode']

        obj.another_address1 = data['another_address1']
        obj.another_address2 = data['another_address2']
        obj.another_city = data['another_city']
        obj.another_state = data['another_state']
        obj.another_zipcode = data['another_zipcode']
        obj.another_country = data['another_country']

        obj.payment_details = data['payment_details']

        obj.email_address1 = data['email_address1']
        obj.email_address2 = data['email_address2']
        obj.email_address3 = data['email_address3']
        obj.website1 = data['website1']
        obj.website2 = data['website2']
        obj.website3 = data['website3']
        obj.mobile1 = data['mobile1']
        obj.mobile2 = data['mobile2']
        obj.mobile3 = data['mobile3']

        obj.profile_link = generate_profile_link(username)
        obj.is_profile_link_active = data['is_profile_link_active']
        obj.is_profile_status_active = data['is_profile_status_active']
        obj.is_profile_editing_active = data['is_profile_editing_active']
        obj.save()

        main_obj.users_list.add(obj)
        main_obj.successful_count += 1
        main_obj.save()

        return {"status": True, "message": "SUCCESS"}
