from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from yarnlibrarybackend import settings
from .serializer import ContactSerializer, UserSerializer, NewsSerializer, ExhibitionSerializer, ProductSerializer
from .models import Contact, User, Roles, News, Exhibition, Product
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from .permissions import IsAdminRole
from django.template.loader import render_to_string
import threading
from django.core.mail import EmailMultiAlternatives
from authentication.utils import send_email

class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role']
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'], permission_classes=[IsAdminRole])
    def supplier(self, request):
        role = Roles.objects.get(name='Supplier')
        serializer = self.get_serializer(data=request.data)
        email = request.data.get('email')
        if(serializer.is_valid()):
            serializer.save(role=role)

            frontend_domain = settings.FRONTEND_URL
            validation_url = f'{frontend_domain}/auth/verify-email/{raw_token}'

            html_content = render_to_string("email/email_verification.html", context={'validation_url':validation_url, username: request.data.get('username')})
            
            email_msg = EmailMultiAlternatives(
                subject="Verify Email Address",
                to=[email],
            )

            email_msg.attach_alternative(html_content, "text/html")

            print("sending verification email to:", email)
            threading.Thread(target=send_email,args=(email_msg,), daemon=True).start()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        role = Roles.objects.get(name='User')
        # serializer = self.get_serializer(data=serializer.data)
        email = serializer.validated_data.get('email')
        if(serializer.is_valid()):
            user = serializer.save(role=role)

            frontend_domain = settings.FRONTEND_URL
            validation_url = f'{frontend_domain}/auth/verify-email/{user.id}'

            html_content = render_to_string("email/email_verification.html", context={'validation_url':validation_url, 'username': user.username})
            
            email_msg = EmailMultiAlternatives(
                subject="Verify Email Address",
                to=[email],
            )

            email_msg.attach_alternative(html_content, "text/html")

            print("sending verification email to:", email)
            threading.Thread(target=send_email,args=(email_msg,), daemon=True).start()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()
    permission_classes = [AllowAny]

class NewsViewSet(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    queryset = News.objects.all()

    def get_permissions(self):
        if(self.action in ['create', 'update', 'partial_update', 'destroy']):
            return [IsAdminRole()]
        else:
            return [AllowAny()]

class ExhibitionViewSet(viewsets.ModelViewSet):
    serializer_class = ExhibitionSerializer
    queryset = Exhibition.objects.all()
    
    def get_permissions(self):
        if(self.action in ['create', 'update', 'partial_update', 'destroy']):
            return [IsAdminRole()]
        else:
            return [AllowAny()]

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    
    def get_permissions(self):
        if(self.action in ['create', 'update', 'partial_update', 'destroy']):
            return [IsAdminRole()]
        else:
            return [AllowAny()]
