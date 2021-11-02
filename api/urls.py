from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.apiOverview, name="api-overview"),
    path('user-list/', views.userlist, name="user-list"),
    path('users/', views.user_register, name="register"),
    path('users/login', obtain_auth_token, name="login"),
    path('users/details', views.user_detail, name="user-detail"),
]