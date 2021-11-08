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

def get_user(request):
    authorization = request.META.get('HTTP_AUTHORIZATION', '')  # get authorization from request header
    token = re.match('Token (.*)', authorization)  # find token in authorization
    if token:
        token = token.group(1)

    user = Token.objects.get(key=token).user  # get user by using token
    return user

@api_view(['GET'])
def userlist(request):                              # check all user
    users = User.objects.all()                      # get all user from user model
    serializer = UserSerializer(users,many=True)    # serialize User model to UserSerializer
    return Response(serializer.data)

@api_view(['POST'])
def user_register(request):
    if request.method=='POST':
        data = {}
        serializer = UserSerializer(data=request.data)  # serialize request data to UserSerializer
        if serializer.is_valid():
            user = serializer.save()                    # save the data
            data['code'] = 200
            data['message']='successful operation'
            token = Token.objects.get(user=user).key    # get user Token from Token model
            data['data'] = {
                "token":token,
            }
        else:
            data['code'] = 400
            messages = []
            for key,value in serializer.errors.items():
                messages.append(value[0])
            data['message'] = messages
        return Response(data)

@api_view(['POST'])
def user_login(request):
    data = {}
    if request.method=='POST':
        userName = request.data['userName']
        password = request.data['password']
        user = User.objects.get_by_natural_key(userName)
        if user.check_password(password):
            data['code'] = 200
            data['message']='successful operation'
            data['data']={
                "token":Token.objects.get(user_id=user.id).key
            }
        else:
            data['code'] = 404
            data['message'] = 'wrong password or wrong username'
        return Response(data)

@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_details(request):
    data = {}
    if request.method=='GET':
        user = get_user(request)                    # get user by using token
        data['code'] = 200
        data['message'] = 'successful operation'
        data['data'] = {
            "username": user.userName,
            "userEmail": user.userEmail,
            "userImage": user.userImage.url,
            "userPhone": user.userPhone
        }
        return Response(data)
    elif request.method=='POST':
        user = get_user(request)
        # request = JSONParser().parse(request)
        serializer = UpdateUserSerializer(user,data=request.data)
        if serializer.is_valid():
            user = serializer.save()                    # save the data
            data['code'] = 200
            data['message'] = 'successful operation'
        else:
            data['code'] = 400
            messages = []
            for key, value in serializer.errors.items():
                messages.append(value[0])
            data['message'] = messages
        return Response(data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_password(request):
    data = {}
    if request.method=='POST':
        user = get_user(request)
        serializer = UpdateUserPasswordSerializer(user,data=request.data)
        if (serializer.is_valid())&(user.check_password(request.data['oldPassword'])):
            user = serializer.save()                    # save the data
            data['code'] = 200
            data['message'] = 'successful operation'
        else:
            data['code'] = 400
            data['message'] = 'wrong password'
        return Response(data)



