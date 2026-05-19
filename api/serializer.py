from rest_framework import serializers
from .models import Contact, User, News, Exhibition, Product
from uploads.utils import get_file_url

class UserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)
    # email = serializers.EmailField(unique=True)
    role_name = serializers.CharField(source='role.name', read_only=True)
    logo_url = serializers.SerializerMethodField()
    confirm_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["id", "username", "email", "company", "phone_number", "address", "logo", "role", "role_name", "is_active", "logo_url", "confirm_password", "password"]

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        self.password = validated_data.get('password')
        user = User.objects.create(**validated_data)
        user.set_password(self.password)
        user.is_active = False
        user.save()

        return user
    
    def get_logo_url(self, obj):
        if obj.logo:
            return get_file_url(obj.logo)
        return None
    
    def validate(self, data):
        print(data)
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def activate(self, user):
        user.is_active = True
        user.save()

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Contact

class NewsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user_id.username', read_only=True)
    image_url = serializers.SerializerMethodField()
    class Meta:
        fields = '__all__'
        model = News

    def get_image_url(self, obj):
        if(obj.image):
            return get_file_url(obj.image)
        return None

class ExhibitionSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user_id.username', read_only=True)
    image_url = serializers.SerializerMethodField()
    class Meta:
        fields = '__all__'
        model = Exhibition

    def get_image_url(self, obj):
        if(obj.image):
            return get_file_url(obj.image)
        return None
        
class ProductSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier_id.username', read_only=True)
    image_urls = serializers.SerializerMethodField()
    class Meta:
        fields = '__all__'
        model = Product

    def get_image_urls(self, obj):
        if(len(obj.images) > 0):
            return [get_file_url(img) for img in obj.images]
        return None