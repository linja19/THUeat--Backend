from django.shortcuts import render

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializer import *
from .permissions import *
from .format import *

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
                first_login = False
            elif user.is_staff:
                type = "staff"
                first_login = Staff.objects.get(user=user.pk).first_login
            else:
                data["code"] = 404
                data["message"] = "public user"
                return Response(data)
            if user.check_password(password):
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
    # select 1 lowercase
    password = random.choice(string.ascii_lowercase)
    # select 1 uppercase
    password += random.choice(string.ascii_uppercase)

    # generate other characters
    for i in range(4):
        password += random.choice(random_source)

    password_list = list(password)
    # shuffle all characters
    random.SystemRandom().shuffle(password_list)
    password = ''.join(password_list)
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
                data['code'] = 200
                data['message'] = 'successful operation'
                token = Token.objects.get(user=user).key
                data['data'] = {
                    "token":token,
                    "userName" :user.userName,
                    "staffName":staff.staffName,
                    "staffPhone":user.userPhone,
                    "staffPassword":password
                }
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
        user_data = {
            "userName": request.data["adminName"],
            "userPhone": request.data["adminPhone"],
            "password": password
        }
        userserializer = UserRegisterSerializer(data=user_data)
        if userserializer.is_valid():
            user = userserializer.save()
            user.is_admin = True
            user.save()
            data['code'] = 200
            data['message'] = 'successful operation'
            token = Token.objects.get(user=user).key
            data['data'] = {
                "token": token,
                "adminName": user.userName,
                "adminPhone": user.userPhone,
                "adminPassword": password
            }
        else:
            data["code"] = 400
            data["message"] = "用户名已存在"
    elif request.method=="GET":
        admin_list = User.objects.filter(is_admin=True)
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