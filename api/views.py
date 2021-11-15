from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.parsers import JSONParser
from .models import User, Token
from .serializer import *
import re

# Create your views here.

def get_user_by_request_token(request):
    authorization = request.META.get('HTTP_AUTHORIZATION', '')  # get authorization from request header
    token = re.match('Token (.*)', authorization)  # find token in authorization
    if token:
        token = token.group(1)

    user = Token.objects.get(key=token).user  # get user by using token
    return user

def get_student_by_user(user):
    user_pk = user.pk                               # get user primary key
    student = Student.objects.get(user=user_pk)     # get student by using user primary key
    return student

def check_email_is_valid(email):
    if Student.objects.filter(userEmail=email).exists():    # check email is exist
        return False
    else:
        return True

@api_view(['GET'])
def userlist(request):                              # check all user
    users = User.objects.all()                      # get all user from user model
    serializer = UserRegisterSerializer(users,many=True)    # serialize User model to UserSerializer
    return Response(serializer.data)

@api_view(['POST'])
def user_register(request):
    if request.method=='POST':
        data = {}                                   # response data
        user_data = {                               # userName,password in User model
            "userName":request.data["userName"],
            "password":request.data["password"]
        }
        userserializer = UserRegisterSerializer(data=user_data) # create userserializer with user_data
        if (userserializer.is_valid())&(check_email_is_valid(request.data["userEmail"])):    # check userserializer is_valid (check user_data), check email is exist
            user = userserializer.save()                # save userserializer (save user to database)
                                                        # create user first as studentserializer need linked to user to create
            student_data = {                            # userEmail in Student model
                "user": user.pk,
                "userEmail": request.data["userEmail"]
            }
            studentserializer = StudentRegisterSerializer(data=student_data)    # create studentserializer with student data
            if studentserializer.is_valid():                                    # check studentserializer is_valid
                studentserializer.save()                                        # save studentserializer (save student to database)
                data['code'] = 200                                              # successful message
                data['message'] = 'successful operation'
                token = Token.objects.get(user=user).key                        # find user in Token model and get its token
                data['data'] = {
                        "token":token,
                    }
            else:
                data['code'] = 400
                data['message'] = "user with this userEmail already exists."    # error userEmail exists
        else:
            data['code'] = 400
            messages = []
            if User.objects.filter(userName=request.data["userName"]).exists(): # error userName exists
                messages.append("用户名已存在")
            if Student.objects.filter(userEmail=request.data["userEmail"]).exists():    # error userEmail exist
                messages.append("用户邮箱已存在")
            data['message'] = messages
        return Response(data)

@api_view(['POST'])
def user_login(request):
    data = {}
    if request.method=='POST':
        userName = request.data['userName']                     # get userName
        password = request.data['password']                     # get password
        try:
            user = User.objects.get_by_natural_key(userName)    # get user by using userName
            if user.check_password(password):                   # check password
                data['code'] = 200
                data['message'] = 'successful operation'
                data['data'] = {
                    "token": Token.objects.get(user_id=user.id).key  # get token by using user_id
                }
            else:
                data['code'] = 404
                data['message'] = '密码错误'
        except:
            data['code'] = 404
            data['message'] = '用户不存在'
        return Response(data)

@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_details(request):
    data = {}
    if request.method=='GET':
        user = get_user_by_request_token(request)                    # get user by using token
        student = get_student_by_user(user)                          # get student
        data['code'] = 200
        data['message'] = 'successful operation'
        data['data'] = {
            "userName": user.userName,
            "userEmail": student.userEmail,
            "userImage": student.userImage.url,
            "userPhone": user.userPhone
        }
        return Response(data)
    elif request.method=='POST':                                    # update user details
        user = get_user_by_request_token(request)                   # get user by token
        student = get_student_by_user(user)                         # get student
        user_data = {
            "userName": request.data["userName"],
            "userPhone": request.data["userPhone"]
        }
        student_data = {
            "user": user.pk,
            "userEmail": request.data["userEmail"],
            # "userImage": request.data["userImage"]
        }
        userserializer = UpdateUserSerializer(user,data=user_data)  # create serializer
        studentserializer = UpdateStudentSerializer(student,data=student_data)
        if (userserializer.is_valid())&(studentserializer.is_valid()):  # check serializer (check data)
            userserializer.save()                    # save serializer (update data)
            studentserializer.save()
            data['code'] = 200
            data['message'] = 'successful operation'
        else:
            data['code'] = 400
            messages = []
            for key, value in userserializer.errors.items():    # get error from serializer
                messages.append(value[0])
            for key, value in studentserializer.errors.items():
                messages.append(value[0])
            data['message'] = messages
        return Response(data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_password(request):
    data = {}
    user = get_user_by_request_token(request)               # get user by token
    user_data = {
        "password": request.data["password"]
    }
    if request.method=='POST':
        serializer = UpdateUserPasswordSerializer(user,data=user_data)      # create serializer
        if (serializer.is_valid())&(user.check_password(request.data['oldPassword'])):      # check old password
            serializer.save()                    # save serializer (update password)
            data['code'] = 200
            data['message'] = 'successful operation'
        else:
            data['code'] = 400
            data['message'] = '旧密码错误'
        return Response(data)



