from api.models import *
from rest_framework import serializers

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userName','userPhone','password']            # field for this serializer (from User model)
        extra_kwargs = {
            'password':{'write_only':True},
        }

    def save(self):                                 # overwrite save function
        user = User(                                # create User object
            userName=self.validated_data['userName'],
            userPhone=self.validated_data['userPhone']
        )
        password = self.validated_data['password']
        user.is_staff = True
        user.set_password(password)                 # set user password
        user.save()
        return user

class StaffRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['user','stallID','staffName']               # field for this serializer (from Student model)

    def save(self):                                 # overwrite save function
        user = self.validated_data["user"]
        stallID = self.validated_data["stallID"]
        staffName = self.validated_data["staffName"]
        staff = Staff(user=user,stallID=stallID,staffName=staffName) # create Student object
        staff.save()
        return staff

class AdminRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['user','adminName']               # field for this serializer (from Student model)

    def save(self):                                 # overwrite save function
        user = self.validated_data["user"]
        adminName = self.validated_data["adminName"]
        admin = Admin(user=user,adminName=adminName) # create Student object
        admin.save()
        return admin

class UpdateUserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_active']

    def update(self, instance, validated_data):  # overwrite update function
        instance.is_active = validated_data['is_active']
        instance.save()
        return instance

class UpdateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userName','userPhone','password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def update(self,instance,validated_data):
        instance.userName = validated_data['userName']
        instance.userPhone = validated_data['userPhone']
        password = validated_data['password']
        instance.set_password(password)
        instance.save()
        return instance

class CreateNoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['noticeImage','noticeTitle','noticeWords']

class CreateStallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stall
        fields = ["stallName","stallFloor","canteenID"]

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyByStaff
        fields = ["parent_reviewID","replyContent","stallID"]

class MystallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stall
        fields = ["stallName","stallFloor","stallDescribe","stallOperationtime"]

class StallImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StallImage
        fields = ["stallImage","stallID"]

class CreateDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ["dishName","dishDescribe","dishPrice","dishImage","dishAvailableTime","stallID","is_active"]

