from rest_framework import serializers
from .models import *
import random
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userName','password']            # field for this serializer (from User model)
        extra_kwargs = {
            'password':{'write_only':True},
        }

    def save(self):                                 # overwrite save function
        user = User(                                # create User object
            userName=self.validated_data['userName']
        )
        password = self.validated_data['password']
        user.set_password(password)                 # set user password
        user.save()
        return user

class StudentRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['user','userEmail']               # field for this serializer (from Student model)

    def save(self):                                 # overwrite save function
        user = self.validated_data["user"]
        verification_number = str(random.randint(0,999999))
        while len(verification_number)!=6:
            verification_number = str(random.randint(0, 999999))
        student = Student(user=user,userEmail=self.validated_data['userEmail'],verificationNumber=verification_number) # create Student object
        student.save()
        return student

class StudentVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['user','verificationNumber']


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userName','userPhone']

    def update(self,instance,validated_data):       # overwrite update function
        instance.userName = validated_data['userName']
        instance.userPhone = validated_data['userPhone']
        instance.save()
        return instance

class UpdateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['userEmail','userImage']
    def update(self,instance,validated_data):       # overwrite update function
        if not instance.userImage.url=='default/default_user.png':
            instance.userImage.delete(save=True)
        instance.userEmail = validated_data['userEmail']
        instance.userImage = validated_data['userImage']
        instance.save()
        return instance

class UpdateStudentEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['userEmail']
    def update(self,instance,validated_data):       # overwrite update function
        instance.userEmail = validated_data['userEmail']
        instance.save()
        return instance

class UpdateUserPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']
        extra_kwargs = {
            'password':{'write_only':True},
        }

    def update(self,instance,validated_data):       # overwrite update function
        password = validated_data['password']
        instance.set_password(password)
        instance.save()
        return instance

class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['reviewComment','reviewTags','stallID','userID','rate']

class CreateReviewImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ["reviewImages","reviewID"]

class DishReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = DishReview
        fields = ["reviewID","dishID"]

class LikeReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeReview
        fields = ["userID","reviewID"]

class LikeDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeDish
        fields = ["userID","dishID"]