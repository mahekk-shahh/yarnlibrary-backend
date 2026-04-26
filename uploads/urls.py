from rest_framework.routers import path
from .views import get_presigned_url

urlpatterns = [
    path('get-presigned-url/', get_presigned_url, name='get_presigned_url'),
]