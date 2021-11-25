from django.shortcuts import render

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializer import *
from .permissions import *
from .format import *
from django.core.mail import send_mail
import threading

@api_view(['POST'])
def login(request):
    data = {}
    if request.method=='POST':
        userName = request.data["name"]
        password = request.data["password"]
        try:
            user = User.objects.get_by_natural_key(userName)
            if user.is_superuser:
                type = "superadmin"
                first_login = False
            elif user.is_admin:
                type = "admin"
                first_login = Admin.objects.get(user=user.pk).first_login
            elif user.is_staff:
                type = "staff"
                first_login = Staff.objects.get(user=user.pk).first_login
            else:
                data["code"] = 404
                data["message"] = "public user"
                return Response(data)
            if user.check_password(password):
                user.save()
                data["code"] = 200
                data["message"] = "successful operation"
                data["data"] = {
                    "token": Token.objects.get(user_id=user.id).key,
                    "firstLogin": first_login,
                    "type": type
                }
            else:
                data["code"] = 400
                data["message"] = "wrong password"
        except:
            data["code"] = 404
            data["message"] = "user not found"

    return Response(data)

import random
import string

def get_random_password():
    random_source = string.ascii_letters + string.digits
    # select 1 lowercase
    password = random.choice(string.ascii_lowercase)
    # select 1 uppercase
    password += random.choice(string.ascii_uppercase)
    # select 1 digit
    password += random.choice(string.digits)

    # generate other characters
    for i in range(4):
        password += random.choice(random_source)

    password_list = list(password)
    # shuffle all characters
    random.SystemRandom().shuffle(password_list)
    password = ''.join(password_list)
    return password

def get_random_username():
    random_source = string.ascii_letters
    # select 1 uppercase
    username = random.choice(string.ascii_uppercase)
    # generate other lowercase characters
    for i in range(4):
        username += random.choice(string.ascii_lowercase)
    # select 1 digit
    username += random.choice(string.digits)

    username_list = list(username)
    password = ''.join(username_list)
    return password

def check_stallID_is_valid(stallID):
    if Stall.objects.filter(stallID=stallID).exists():
        return True
    return False

@api_view(['POST','GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdmin])
def createstaff(request):
    data = {}
    if request.method=='POST':
        username = get_random_username()
        password = get_random_password()
        while User.objects.filter(userName=username).exists():
            username = get_random_username()
        user_data = {
            "userName":username,
            "userPhone":request.data["staffPhone"],
            "password":password
        }
        userserializer = UserRegisterSerializer(data=user_data)
        if (userserializer.is_valid()&check_stallID_is_valid(request.data["stallID"])):
            user = userserializer.save()
            staff_data = {
                "user":user.pk,
                "stallID":request.data["stallID"],
                "staffName":request.data["staffName"]
            }
            staffserializer = StaffRegisterSerializer(data=staff_data)
            if staffserializer.is_valid():
                staff = staffserializer.save()
                staff.staffID = Staff.objects.all().count() + 1
                staff.save()
                content = '''Hi '''+ staff.staffName + ''', this is your account information, visit the website and login. After login, please change your username and password.
                username:''' + username + '''
                password:''' + password  # create email content
                arg = (  # send_mail args
                    "THU-EAT Staff Account",
                    content,
                    settings.EMAIL_HOST_USER,
                    [user.userPhone],
                    True
                )
                t1 = threading.Thread(target=send_mail, args=arg)  # multithreading send verification number to email
                t1.start()
                data['code'] = 200
                data['message'] = 'successful operation'
        else:
            data["code"] = 400
            message = []
            if User.objects.filter(userName=request.data["staffName"]).exists():
                message.append("用户名已存在")
            if not Stall.objects.filter(stallID=request.data["stallID"]).exists():
                message.append("stallID不存在")
            data["message"] = message
    elif request.method=="GET":
        try:
            stallID = request.query_params["stallID"]
            stafflist = Staff.objects.filter(stallID=int(stallID))
            datalist = format_stafflist(stafflist)
        except:
            try:
                canteenID = request.query_params["canteenID"]
                stalllist = Stall.objects.filter(canteenID=int(canteenID))
                list = []
                for stall in stalllist:
                    stafflist = Staff.objects.filter(stallID=stall.stallID)
                    list += format_stafflist(stafflist)
                datalist = list
            except:
                stafflist = Staff.objects.all()
                datalist = format_stafflist(stafflist)


        data["code"] = 200
        data["message"] = "successful operation"
        data["data"] = datalist

    return Response(data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdmin])
def staffstatus(request,staffID):
    data = {}
    if request.method=="POST":
        try:
            user = User.objects.get(id=int(staffID))
            if user.is_admin == True or user.is_superuser == True:
                data["code"] = 400
                data["message"] = "no permission"
                return Response(data)
            if request.data["staffStatus"] == "False" or request.data["staffStatus"] == False:
                status = False
            else:
                status = True
            user_data = {
                "is_active": status
            }
            serializer = UpdateUserStatusSerializer(user, data=user_data)
            if serializer.is_valid():
                serializer.save()
            data["code"] = 200
            data["message"] = "successful operation"
        except:
            data["code"] = 404
            data["message"] = "user not exist"
    return Response(data)

@api_view(['POST','GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsSuperadmin])
def createadmin(request):
    data = {}
    if request.method == 'POST':
        password = get_random_password()
        username = get_random_username()
        while User.objects.filter(userName=username).exists():
            username = get_random_username()
        user_data = {
            "userName": username,
            "userPhone": request.data["adminPhone"],
            "password": password
        }
        userserializer = UserRegisterSerializer(data=user_data)
        if userserializer.is_valid():
            user = userserializer.save()
            user.is_admin = True
            user.save()
            admin_data = {
                "user":user.pk,
                "adminName": request.data["adminValidName"]
            }
            adminserializer = AdminRegisterSerializer(data=admin_data)
            if adminserializer.is_valid():
                admin = adminserializer.save()
                admin.adminID = Admin.objects.all().count()
                admin.save()
                content = '''Hi ''' + admin.adminName + ''', this is your account information, visit the website and login. After login, please change your username and password.
                            username:''' + username + '''
                            password:''' + password  # create email content
                arg = (  # send_mail args
                    "THU-EAT Admin Account",
                    content,
                    settings.EMAIL_HOST_USER,
                    [user.userPhone],
                    True
                )
                t1 = threading.Thread(target=send_mail, args=arg)  # multithreading send verification number to email
                t1.start()
                data['code'] = 200
                data['message'] = 'successful operation'
    elif request.method=="GET":
        admin_list = Admin.objects.all()
        data["code"] = 200
        data["message"] = "successful operation"
        data["data"] = format_adminlist(admin_list)

    return Response(data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsSuperadmin])
def adminstatus(request,adminID):
    data = {}
    if request.method=="POST":
        try:
            user = User.objects.get(id=int(adminID))
            if user.is_superuser:
                data["code"] = 400
                data["message"] = "Superadmin cannot be inactivated"
                return Response(data)
            if request.data["adminStatus"] == "False" or request.data["adminStatus"] == False:
                status = False
            else:
                status = True
            user_data = {
                "is_active": status
            }
            serializer = UpdateUserStatusSerializer(user, data=user_data)
            if serializer.is_valid():
                serializer.save()
            data["code"] = 200
            data["message"] = "successful operation"
        except:
            data["code"] = 404
            data["message"] = 'user not exists'
    return Response(data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdmin])
def userlist(request):
    data = {}
    if request.method=="GET":
        try:
            numbers = request.query_params["numbers"]
            student_list = Student.objects.all()[:int(numbers)]
        except:
            student_list = Student.objects.all()
        data["code"] = 200
        data["message"] = "successful operation"
        data["data"] = format_student_list(student_list)
    return Response(data)

@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdmin])
def userdetails(request,userID):
    data = {}
    if request.method=="GET":
        try:
            student = Student.objects.get(user=int(userID))
            data["code"] = 200
            data["message"] = "successful operation"
            data["data"] = format_student(student)
        except:
            data["code"] = 404
            data["message"] = "user not found"
    elif request.method=="POST":
        try:
            user = User.objects.get(id=int(userID))
            if user.is_admin==True or user.is_superuser==True:
                data["code"] = 400
                data["message"] = "no permission"
                return Response(data)
            if request.data["userStatus"] == "False" or request.data["userStatus"]==False:
                status = False
            else:
                status = True
            user_data = {
                "is_active": status
            }
            serializer = UpdateUserStatusSerializer(user, data=user_data)
            if serializer.is_valid():
                serializer.save()
            data["code"] = 200
            data["message"] = "successful operation"
        except:
            data["code"] = 404
            data["message"] = "user not exist"
    return Response(data)

import re
def get_user_by_request_token(request):
    authorization = request.META.get('HTTP_AUTHORIZATION', '')  # get authorization from request header
    token = re.match('Token (.*)', authorization)  # find token in authorization
    if token:
        token = token.group(1)

    user = Token.objects.get(key=token).user  # get user by using token
    return user

@api_view(['POST','GET'])
def selfdetails(request):
    data = {}
    if request.method=='POST':
        try:
            user = Token.objects.get(key=request.data["token"]).user
        except:
            data["code"] = 400
            data["message"] = "token not provided"
            return Response(data)
        user_data = {
            'userName':request.data["name"],
            'userPhone':request.data["phone"],
            'password':request.data["password"]
        }
        if user.is_admin:
            serializers = UpdateAdminSerializer(user,data=user_data)
            if serializers.is_valid() and user.check_password(request.data["oldPassword"]):
                serializers.save()
                admin = Admin.objects.get(user=user.pk)
                data["code"] = 200
                if admin.first_login:
                    data["message"] = "successful operation, account activated successful"
                    admin.first_login = False
                    user.is_active = True
                    admin.save()
                    user.save()
                else:
                    data["message"] = "successful operation"
            else:
                data["code"] = 200
                if user.check_password(request.data["oldPassword"]):
                    data["message"] = "wrong password"
                else:
                    data["message"] = "username exists"
        elif user.is_staff:
            serializers = UpdateAdminSerializer(user, data=user_data)
            if serializers.is_valid() and user.check_password(request.data["oldPassword"]):
                serializers.save()
                staff = Staff.objects.get(user=user.pk)
                data["code"] = 200
                if staff.first_login:
                    data["message"] = "successful operation, account activated successful"
                    staff.first_login = False
                    user.is_active = True
                    staff.save()
                    user.save()
                else:
                    data["message"] = "successful operation"
            else:
                data["code"] = 200
                data["message"] = "wrong password"
    elif request.method=="GET":
        try:
            user = get_user_by_request_token(request)
            if user.is_superuser:
                validName = ["SuperAdmin"]
                type = "superadmin"
            elif user.is_admin:
                validName = Admin.objects.get(user=user.pk).adminName,
                type = "admin"
            elif user.is_staff:
                validName = Staff.objects.get(user=user.pk).staffName,
                type = "staff"
            else:
                data["code"] = 400
                data["message"] = "public user"
                return Response(data)
            data["code"] = 200
            data["message"] = "successful operation"
            data["data"] = {
                "validName":validName[0],
                "name":user.userName,
                "phone":user.userPhone,
                "type":type
            }
        except:
            data["code"] = 400
            data["message"] = "token not provided"
    return Response(data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdmin])
def adminstatistic(request):
    data = {}
    if request.method=='GET':
        data["code"] = 200
        data["message"] = "successful operation"
        data["data"] = format_admin_statistic()
    return Response(data)

@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdmin])
def notice(request):
    data = {}
    if request.method=='GET':
        notice_list = Notice.objects.all()
        data["code"] = 200
        data["message"] = "successful operation"
        data["data"] = format_notice_list(notice_list)
    elif request.method=="POST":
        noticeserializer = CreateNoticeSerializer(data=request.data)
        if noticeserializer.is_valid():
            noticeserializer.save()
            data["code"] = 200
            data["message"] = "successful operation"
        else:
            data["code"] = 400
            data["message"] = "something wrong"
    return Response(data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdmin])
def canteen(request):
    data = {}
    if request.method=='GET':
        data["code"] = 200
        data["message"] = "successful operation"
        data["data"] = format_canteen()
    return Response(data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdmin])
def canteen_name(request):
    data = {}
    if request.method == 'GET':
        data["code"] = 200
        data["message"] = "successful operation"
        data["data"] = format_canteen_name()
    return Response(data)

@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdmin])
def stalls(request):
    data = {}
    if request.method == 'GET':
        data["code"] = 200
        data["message"] = "successful operation"
        try:
            canteenID = request.query_params["canteenID"]
            stall_list = Stall.objects.filter(canteenID=canteenID)
        except:
            stall_list = Stall.objects.all()
        try:
            if request.query_params["status"]=="True":
                status = True
            elif request.query_params["status"]=="False":
                status = False
            stall_list = stall_list.filter(is_active=status)
        except:
            pass
        data["data"] = format_stall_list(stall_list)
    elif request.method == 'POST':
        stallserializer = CreateStallSerializer(data=request.data)
        if stallserializer.is_valid():
            stallserializer.save()
            data["code"] = 200
            data["message"] = "successful operation"
        else:
            data["code"] = 400
            data["message"] = "canteenID not exists"
    return Response(data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdmin])
def stalls_status(request,stallID):
    data = {}
    if request.method=="POST":
        try:
            stall = Stall.objects.get(stallID=stallID)
            if request.data["stallStatus"] == True:
                stall.is_active = True
                stall.save()
                data["code"] = 200
                data["message"] = "successful operation"
            elif request.data["stallStatus"] == False:
                stall.is_active = False
                stall.save()
                data["code"] = 200
                data["message"] = "successful operation"
        except:
            data["code"] = 400
            data["message"] = "stallID not exists"
    return Response(data)