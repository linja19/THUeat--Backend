from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password','userEmail']
        extra_kwargs = {
            'password':{'write_only':True},
        }

    def save(self):
        user = User(
            userEmail=self.validated_data['userEmail'],
            username=self.validated_data['username']
        )
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','userEmail','userImage','userPhone']
        # extra_kwargs = {
        #     'password':{'write_only':True},
        # }

    def update(self,instance,validated_data):
        instance.username = validated_data['username']
        instance.userEmail = validated_data['userEmail']
        instance.userPhone = validated_data['userPhone']
        instance.userImage = validated_data['userImage']
        instance.save()
        return instance

class UpdateUserPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']
        extra_kwargs = {
            'password':{'write_only':True},
        }

    def update(self,instance,validated_data):
        password = validated_data['password']
        instance.set_password(password)
        instance.save()
        return instance