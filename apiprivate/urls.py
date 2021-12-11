from django.urls import path, include
from . import views

urlpatterns = [
    path('authorization', views.login, name="login"),
    path('details', views.selfdetails, name="user-detail"),
    path('staffs', views.createstaff, name="create-staff"),
    path('staffs/<int:staffID>', views.staffstatus, name="staff-status"),
    path('admins', views.createadmin, name="create-admin"),
    path('admins/<int:adminID>', views.adminstatus, name="admin-status"),
    path('users', views.userlist, name="user-list"),
    path('users/<int:userID>', views.userdetails, name="user-details"),
    path('adminStatistics', views.adminstatistic, name="admin-statistics"),
    path('notices', views.notice, name="notice"),
    path('notices/<noticeID>', views.delete_notice, name="delete-notice"),
    path('canteens', views.canteen, name="canteen"),
    path('canteens/names', views.canteen_name, name="canteen-name"),
    path('stalls', views.stalls, name="stall"),
    path('stalls/<stallID>', views.stalls_status, name="stall-status"),
    path('mystall', views.mystall, name="mystall"),
    path('mystall/reviews', views.mystall_review, name="mystall-review"),
    path('mystall/reviews/<reviewID>', views.create_reply, name="create-reply"),
    path('mystall/dishes', views.dish, name="dish"),
    path('mystall/dishes/<dishID>', views.dish_detail, name="dish-detail"),
]