from django.urls import path
from .views import login, get_access_token, logout, ResetPasswordTokenView, NewPasswordView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('forgot-password', ResetPasswordTokenView, basename='forgot-password/')
router.register('reset-password', NewPasswordView, basename='reset-password')

urlpatterns = router.urls

urlpatterns += [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('access/', get_access_token, name='access'),
]
