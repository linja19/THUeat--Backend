from django.urls import path, include
from . import views

urlpatterns = [
    path('authorization', views.login, name="login"),
]