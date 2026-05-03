from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
import hashlib
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from .serializer import LoginSerializer, ResetPasswordTokenSerializer, NewPasswordSerializer
from .models import ResetPasswordToken
from .utils import generate_reset_token
from api.models import User


# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Login endpoint that authenticates a user and returns a token.
    
    Expected request data:
    {
        "email": "user@example.com",
        "password": "password"
    }
    
    Returns:
    {
        "token": "<auth_token>",
        "user": {
            "id": 1,
            "username": "username",
            "email": "user@example.com",
            "company": "Company Name",
            "phone_number": "1234567890",
            "address": "Address",
            "logo": "logo_url",
            "role": 1,
            "role_name": "Supplier",
            "is_active": true,
            "logo_url": "full_url_to_logo"
        }
    }
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        refresh = RefreshToken.for_user(user)

        response = Response({
            'access': str(refresh.access_token),
            'user': str(user)
        }, status=status.HTTP_200_OK)

        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            max_age= 7 * 24 * 60 * 60,
            samesite='Lax',
            secure=False
        )

        return response
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
@api_view(['GET'])
@permission_classes([AllowAny])
def get_access_token(request):
    refresh_token = request.COOKIES.get('refresh_token')
    
    if not refresh_token:
        return Response({
            'message': 'No token found',
            'access': None,
            'is_authenticated': False
        }, status=status.HTTP_401_UNAUTHORIZED)

    try:
        access = RefreshToken(refresh_token)

        return Response({
            'access': str(access.access_token),
            'is_authenticated': True
        })
    except Exception:
        return Response({
            'message': 'Invalid token',
            'access': None,
            'is_authenticated': False,
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([AllowAny])
def logout(request):
    try:
        refresh_token = request.COOKIES.get('refresh_token')
        if(refresh_token):
            token = RefreshToken(refresh_token)
            token.blacklist()
    # Pass even if n token is found
    except Exception as error:
        pass
    response = Response(status=status.HTTP_200_OK)
    response.delete_cookie(
        key='refresh_token',
        path='/',
        samesite='Lax',
    )
    
    return response

class ResetPasswordTokenView(viewsets.ModelViewSet):
    queryset = ResetPasswordToken.objects.all()
    serializer_class = ResetPasswordTokenSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')

        user = User.objects.filter(email = email).first()

        if user:
            raw_token, hashed_token = generate_reset_token()
            ResetPasswordToken.objects.create(user=user, token=hashed_token)
            frontend_domain = settings.FRONTEND_URL
            reset_link = f'{frontend_domain}/reset-password/{raw_token}'

            html_content = render_to_string("email/reset_password.html", context={'reset_link':reset_link, 'frontend_domain':frontend_domain})
            email = EmailMultiAlternatives(
                subject="Reset Password",
                to=["mahek240305@gmail.com"],
            )
            email.attach_alternative(html_content, "text/html")

            email.send()

        return Response(
            {
                "message": "A password reset link has been sent. Kindly check your inbox and spam folder. If the email is not received, please verify the email address and try again."
            },
            status=status.HTTP_200_OK
        )

class NewPasswordView(viewsets.ModelViewSet):
    serializer_class = NewPasswordSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        token = request.data.get("token")
        hashed = hashlib.sha256(token.encode()).hexdigest()

        reset_password_obj = ResetPasswordToken.objects.filter(token = hashed).first()

        if not reset_password_obj or not reset_password_obj.is_valid(token):
            return Response(
                {"message": "The password reset link is invalid or has expired."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        password = request.data.get("password")

        user = reset_password_obj.user
        user.set_password(password)
        user.save()

        reset_password_obj.deactivate()

        return Response(
            {"message": "Your password has been reset successfully. Please log in with your new credentials."},
            status=status.HTTP_200_OK
        )