from django.urls import path, include
from . import views

urlpatterns = [
    path('authorization', views.login, name="login"),
    path('staffs', views.createstaff, name="create-staff"),
    path('staffs/<int:staffID>', views.staffstatus, name="staff-status"),
    path('admins', views.createadmin, name="create-admin"),
    path('admins/<int:adminID>', views.adminstatus, name="admin-status"),
    path('users', views.userlist, name="user-list"),
    path('users/<int:userID>', views.userdetails, name="user-details"),
]