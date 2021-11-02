from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from .models import User, Token
from .serializer import UserSerializer
import re

# Create your views here.

@api_view(['GET'])
def apiOverview(request):   # check all api
    api_urls = {
        'List':'/task-list/',
    }
    return Response(api_urls)

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
            data['response']='successful'
            token = Token.objects.get(user=user).key    # get user Token from Token model
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)

@api_view(['GET','PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_detail(request):
    data = {}
    if request.method=='GET':
        user = get_user(request)                    # get user by using token
        data['username'] = user.username
        data['userEmail'] = user.email
        data['userImage'] = user.profile_pic.url
        return Response(data)
    # elif request.method=='PUT':
    #     user = get_user(request)
    #     new_data = JSONParser().parse(request)
    #     serializer = UserSerializer(user,data=new_data)
    #     if serializer.is_valid():
    #         user = serializer.save()                    # save the data
    #         data['response']='successful'
    #     else:
    #         data = serializer.errors
    #     return Response(data)

def get_user(request):
    authorization = request.META.get('HTTP_AUTHORIZATION', '')  # get authorization from request header
    token = re.match('Token (.*)', authorization)  # find token in authorization
    if token:
        token = token.group(1)

    user = Token.objects.get(key=token).user  # get user by using token
    return user