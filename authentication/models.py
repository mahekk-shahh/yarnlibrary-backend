from django.db import models
from api.models import User
from django.utils import timezone
from datetime import timedelta
import hashlib

# Create your models here.
class ResetPasswordToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user')
    token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'reset_password_token'
        
    def __str__(self):
        return self.user.email
    
    def save(self, *args, **kwargs):
        self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)
    
    def is_valid(self, raw_token):
        hashed = hashlib.sha256(raw_token.encode()).hexdigest()
        return self.is_active and self.expires_at > timezone.now() and hashed == self.token
    
    def deactivate(self):
        self.is_active = False
        self.save()