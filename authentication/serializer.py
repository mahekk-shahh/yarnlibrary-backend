from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import ResetPasswordToken
from api.models import User
import threading
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .utils import send_email

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            existing_user = User.objects.filter(email=email).first()
            if not existing_user.is_active:
                frontend_domain = settings.FRONTEND_URL
                verification_url = f'{frontend_domain}/auth/verify-email/{existing_user.id}'

                print(verification_url)

                html_content = render_to_string("email/email_verification.html", context={'verification_url':verification_url, 'username': existing_user.username})
                
                email_msg = EmailMultiAlternatives(
                    subject="Verify Email Address",
                    to=[email],
                )

                email_msg.attach_alternative(html_content, "text/html")

                print("sending verification email to:", email)
                threading.Thread(target=send_email,args=(email_msg,), daemon=True).start()
                raise serializers.ValidationError(
                    "Your account is pending email verification. A new verification link has been sent to your registered email address."
                )

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