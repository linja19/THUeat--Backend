from django.urls import path, include
from . import views
# from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('user-list/', views.userlist, name="user-list"),
    path('users/', views.user_register, name="register"),
    path('authorization', views.user_login, name="login"),
    path('users/details', views.user_details, name="user-detail"),
    path('users/password', views.user_password, name="user-detail-password"),
]