from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializer import ContactSerializer, UserSerializer, NewsSerializer, ExhibitionSerializer, ProductSerializer
from .models import Contact, User, Roles, News, Exhibition, Product
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from .permissions import IsAdminRole

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
        if(serializer.is_valid()):
            serializer.save(role=role)
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
