from django.urls import path, include
from . import views

urlpatterns = [
    path('authorization', views.login, name="login"),
    path('staffs', views.createstaff, name="create-staff"),
]