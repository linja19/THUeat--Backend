from django.shortcuts import render

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializer import *
from .permissions import *

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

def check_stallID_is_valid(stallID):
    if Stall.objects.filter(stallID=stallID).exists():
        return True
    return False

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdmin])
def createstaff(request):
    data = {}
    if request.method=='POST':
        password = get_random_password()
        user_data = {
            "userName":request.data["staffName"],
            "userPhone":request.data["staffPhone"],
            "password":password
        }
        userserializer = UserRegisterSerializer(data=user_data)
        if (userserializer.is_valid()&check_stallID_is_valid(request.data["stallID"])):
            user = userserializer.save()
            staff_data = {
                "user":user.pk,
                "stallID":request.data["stallID"],
            }
            staffserializer = StaffRegisterSerializer(data=staff_data)
            if staffserializer.is_valid():
                staffserializer.save()
                data['code'] = 200
                data['message'] = 'successful operation'
                token = Token.objects.get(user=user).key
                data['data'] = {
                    "token":token,
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

    return Response(data)