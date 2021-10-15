from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializer import UserSerializer

# Create your views here.

@api_view(['GET'])
def apiOverview(request):   # check all api
    api_urls = {
        'List':'/task-list/',
    }
    return Response(api_urls)

@api_view(['GET'])
def userlist(request):      # check all user
    users = User.objects.all()
    serializer = UserSerializer(users,many=True)
    return Response(serializer.data)