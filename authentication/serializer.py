from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import ResetPasswordToken
from api.models import User
from .utils import generate_reset_token

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                raise serializers.ValidationError('Invalid email or password.')
        else:
            raise serializers.ValidationError('Email and password are required.')
        
        data['user'] = user
        return data
    
class ResetPasswordTokenSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    class Meta:
        model = ResetPasswordToken
        fields = ['email']

class NewPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(max_length = 50)
    confirm_password = serializers.CharField(max_length = 50)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data