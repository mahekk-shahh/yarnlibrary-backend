from tokenize import String

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

class Roles(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'roles'

class User(AbstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    company = models.CharField(max_length=100, unique=True)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, blank=True, default=2)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    logo = models.TextField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'company']
    
    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'users'

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    mobile_number = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'contact'

class News(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.TextField()
    tags = ArrayField(models.CharField(max_length=50), default=list)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'news'

class Exhibition(models.Model):
  title = models.CharField(max_length=50)
  description = models.TextField(null=True, blank=True)
  venue = models.CharField(max_length=100)
  start_date = models.DateField()
  end_date = models.DateField()
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)
  image = models.TextField()

  def __str__(self):
    return self.title
  
  class Meta:
    db_table = 'exhibitions'

class Product(models.Model):
    name = models.CharField(max_length=100)
    quality = models.CharField(max_length=100, null=True, blank=True)
    count = models.CharField(max_length=100, null=True, blank=True)
    blend = models.CharField(max_length=100, null=True, blank=True)
    shade = models.CharField(max_length=100, null=True, blank=True)
    featured = models.BooleanField(default=False)
    images = ArrayField(models.CharField(max_length=200), default=list)
    supplier_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'products'