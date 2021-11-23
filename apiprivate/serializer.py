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
        fields = ['user','stallID']               # field for this serializer (from Student model)

    def save(self):                                 # overwrite save function
        user = self.validated_data["user"]
        stallID = self.validated_data["stallID"]
        staff = Staff(user=user,stallID=stallID) # create Student object
        staff.save()
        return staff