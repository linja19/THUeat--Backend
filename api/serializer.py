from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password','email')
        extra_kwargs = {
            'password':{'write_only':True},
        }

    def save(self):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username']
        )
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user
