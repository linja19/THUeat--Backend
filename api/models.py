from django.db import models

# Create your models here.

class User(models.Model):
    student_ID = models.IntegerField()
    username = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)