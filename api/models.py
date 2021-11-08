from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid,os
# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self,userEmail,username,password=None):
        if not userEmail:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            userEmail=self.normalize_email(userEmail),
            userName=username,
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, userEmail, username, password):
        user = self.create_user(
            userEmail=self.normalize_email(userEmail),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

def get_file_path_user(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("user",filename)

class User(AbstractBaseUser):
    # userPassword = models.CharField(default='NULL',max_length=128, verbose_name='password')
    #
    username = models.CharField(max_length=30,unique=True)
    userEmail = models.EmailField(verbose_name="email",max_length=100,unique=True)
    userPhone = models.CharField(max_length=30,null=True)
    userImage = models.ImageField(upload_to=get_file_path_user,default="default/default_user.png",null=True,blank=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['userEmail']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)


def get_file_path_canteen(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("user",filename)

class Canteen(models.Model):
    canteenID = models.BigAutoField(primary_key=True)
    canteenName = models.CharField(max_length=30,unique=True)
    canteenAddress = models.CharField(max_length=60)
    canteenImage = models.ImageField(upload_to=get_file_path_canteen,default="default/default_canteen.jpg",null=True,blank=True)
    canteenIntro = models.CharField(max_length=300,blank=True)
    canteenType = models.IntegerField()
    canteenOperationTime = models.CharField(max_length=100,blank=True)

def get_file_path_stall(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("stall",filename)

class Stall(models.Model):
    stallID = models.BigAutoField(primary_key=True)
    stallName = models.CharField(max_length=30,unique=True)
    stallAddress = models.CharField(max_length=60)
    stallImage = models.ImageField(upload_to=get_file_path_stall,default="default/default_stall.jpg",null=True,blank=True)
    stallDescribe = models.CharField(max_length=300,blank=True)
    stallRate = models.FloatField(blank=True)
    stallRateNum = models.IntegerField(blank=True)
    canteenID = models.ForeignKey(Canteen,on_delete=models.CASCADE)

def get_file_path_dish(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("dish",filename)

class Dish(models.Model):

    AVAILABLE_TIME_CHOICES = [
        ("1", "Breakfast"),
        ("2", "Lunch"),
        ("3", "Dinner"),
        ("4", "Supper")
    ]

    dishID = models.BigAutoField(primary_key=True)
    dishName = models.CharField(max_length=30, unique=True)
    dishPrice = models.FloatField()
    dishImage = models.ImageField(upload_to=get_file_path_dish, default="default/default_dish.jpg", null=True,
                                   blank=True)
    dishDescribe = models.CharField(max_length=300, blank=True)
    dishLikes = models.IntegerField(blank=True)
    dishAvailableTime = models.CharField(max_length=4, default='1234')
    stallID = models.ForeignKey(Stall,on_delete=models.CASCADE)

def get_file_path_review(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("review",filename)

class Review(models.Model):
    reviewID = models.BigAutoField(primary_key=True)
    reviewDateTime = models.DateTimeField(auto_now=True)
    reviewLikes = models.IntegerField(blank=True)
    reviewComment = models.CharField(max_length=500,blank=True)
    reviewImages = models.ImageField(upload_to=get_file_path_review, null=True,
                                   blank=True)
    reviewTags = models.CharField(max_length=100,blank=True)
    reply = models.BooleanField(default=False)
    stallID = models.ForeignKey(Stall,on_delete=models.CASCADE)
    userID = models.ForeignKey(User,on_delete=models.CASCADE)

class DishReview(models.Model):
    reviewID = models.ForeignKey(Review,on_delete=models.CASCADE)
    dishID = models.ForeignKey(Dish,on_delete=models.CASCADE)

class LikeReview(models.Model):
    userID = models.ForeignKey(User,on_delete=models.CASCADE)
    reviewID = models.ForeignKey(Review, on_delete=models.CASCADE)

class LikeDish(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    dishID = models.ForeignKey(Dish, on_delete=models.CASCADE)

class UserStall(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    stallID = models.ForeignKey(Stall, on_delete=models.CASCADE)

class Ratings(models.Model):
    stallRate = models.FloatField()
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    stallID = models.ForeignKey(Stall, on_delete=models.CASCADE)