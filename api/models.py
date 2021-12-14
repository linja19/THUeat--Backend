from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid,os
# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self,userName,password=None):

        if not userName:
            raise ValueError('Users must have a username')

        user = self.model(

            userName=userName,
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, userName, password):
        user = self.create_user(
            # userEmail=self.normalize_email(userEmail),
            password=password,
            userName=userName,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

def get_file_path_user(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("user",filename)

class User(AbstractBaseUser):

    userName = models.CharField(max_length=30,unique=True)
    userPhone = models.CharField(max_length=30,null=True,blank=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'userName'
    REQUIRED_FIELDS = []

    objects = MyAccountManager()

    def __str__(self):
        return self.userName

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    userImage = models.ImageField(upload_to=get_file_path_user,default="default/default_user.png",null=True,blank=True)
    userEmail = models.EmailField(max_length=100, unique=True)
    verificationNumber = models.CharField(max_length=6,default=None)
    def __str__(self):
        return str(self.user)

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)


def get_file_path_canteen(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("canteens",filename)

class Canteen(models.Model):
    canteenID = models.BigAutoField(primary_key=True)
    canteenName = models.CharField(max_length=30,unique=True)
    canteenAddress = models.CharField(max_length=60)
    canteenImage = models.ImageField(upload_to=get_file_path_canteen,default="default/default_canteen.jpg",null=True,blank=True)
    canteenIntro = models.CharField(max_length=300,blank=True)
    canteenType = models.IntegerField()
    canteenOperationTime = models.CharField(max_length=100,blank=True)
    canteenPhone = models.CharField(max_length=30,default=None)
    canteenFloor = models.CharField(max_length=10,default=None)

    def __str__(self):
        return self.canteenName

def get_file_path_stall(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("stall",filename)

class Stall(models.Model):
    stallID = models.BigAutoField(primary_key=True)
    stallName = models.CharField(max_length=30)
    stallFloor = models.IntegerField(null=True)
    stallDescribe = models.CharField(max_length=300,blank=True)
    stallRate = models.FloatField(blank=True,null=True)
    stallRateNum = models.IntegerField(blank=True,null=True,default=0)
    canteenID = models.ForeignKey(Canteen,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    stallOperationtime = models.CharField(max_length=100,default=None,blank=True,null=True)

    def __str__(self):
        return self.stallName

class StallImage(models.Model):
    stallImage = models.ImageField(upload_to=get_file_path_stall,default="default/default_stall.png",null=True,blank=True)
    stallID = models.ForeignKey(Stall,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.stallID)

class Staff(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    first_login = models.BooleanField(default=True)
    stallID = models.ForeignKey(Stall, on_delete=models.CASCADE, default=None)
    staffName = models.CharField(max_length=10,default=None)
    staffID = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)

class Admin(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    first_login = models.BooleanField(default=True)
    adminName = models.CharField(max_length=10,default=None)
    adminID = models.IntegerField(default=0)

    def __str__(self):
        return str(self.adminName)

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
    dishName = models.CharField(max_length=30)
    dishPrice = models.FloatField()
    dishImage = models.ImageField(upload_to=get_file_path_dish, default="default/default_dish.jpg", null=True,
                                   blank=True)
    dishDescribe = models.CharField(max_length=300, blank=True)
    dishLikes = models.IntegerField(default=0,blank=True,null=True)
    dishAvailableTime = models.CharField(max_length=15, default='1234')
    stallID = models.ForeignKey(Stall,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.dishPrice = round(self.dishPrice, 2)
        super(Dish, self).save(*args, **kwargs)

    def __str__(self):
        return self.dishName

class DishImage(models.Model):
    dishImage = models.ImageField(upload_to=get_file_path_dish,default="default/default_dish.png",null=True,blank=True)
    dishID = models.ForeignKey(Dish,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.dishID)

def get_file_path_review(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("review",filename)

class Review(models.Model):
    reviewID = models.BigAutoField(primary_key=True)
    reviewDateTime = models.DateTimeField(auto_now_add=True)
    reviewLikes = models.IntegerField(default=0,blank=True,null=True)
    reviewComment = models.CharField(max_length=500,blank=True)
    reviewTags = models.CharField(max_length=100,blank=True)
    reply = models.BooleanField(default=False)
    rate = models.FloatField(default=None)
    stallID = models.ForeignKey(Stall,on_delete=models.CASCADE)
    userID = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        name = str(self.userID)+'_'+str(self.stallID)
        return name

class ReplyByStaff(models.Model):
    parent_reviewID = models.ForeignKey(Review,on_delete=models.CASCADE)
    stallID = models.ForeignKey(Stall,on_delete=models.CASCADE)
    replyContent = models.CharField(max_length=500,blank=True)
    replyDateTime = models.DateTimeField(auto_now_add=True)

class ReviewImage(models.Model):
    reviewImages = models.ImageField(upload_to=get_file_path_review, null=True,
                                   blank=True)
    reviewID = models.ForeignKey(Review,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.reviewID)

class DishReview(models.Model):
    reviewID = models.ForeignKey(Review,on_delete=models.CASCADE)
    dishID = models.ForeignKey(Dish,on_delete=models.CASCADE)

    def __str__(self):
        name = str(self.reviewID)+'_'+str(self.dishID)
        return name

class LikeReview(models.Model):
    userID = models.ForeignKey(User,on_delete=models.CASCADE)
    reviewID = models.ForeignKey(Review, on_delete=models.CASCADE)

    def __str__(self):
        name = str(self.userID)+'_'+str(self.reviewID)
        return name

class LikeDish(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    dishID = models.ForeignKey(Dish, on_delete=models.CASCADE)

    def __str__(self):
        name = str(self.userID)+'_'+str(self.dishID)
        return name

def get_file_path_notice(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("notice",filename)

class Notice(models.Model):
    ADS = "ADVERTISEMENT"
    NOTICE = "NOTICE"
    CHOICES = (
        (ADS,"ADVERTISEMENT"),
        (NOTICE,"NOTICE")
    )

    noticeImage = models.ImageField(upload_to=get_file_path_notice, null=True,
                                   blank=True,default="default/default_notice.jpg")
    # noticeCreateTime = models.DateTimeField(auto_created=True)
    # noticeType = models.CharField(max_length=20,choices=CHOICES)
    noticeTitle = models.CharField(max_length=60,default=None)
    noticeWords = models.CharField(max_length=150,default=None)

    def __str__(self):
        return self.noticeTitle