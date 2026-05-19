from django.urls import path
from .views import login, get_access_token, logout, admin_login, activate_user, ResetPasswordTokenView, NewPasswordView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('forgot-password', ResetPasswordTokenView, basename='forgot-password/')
router.register('reset-password', NewPasswordView, basename='reset-password')

urlpatterns = router.urls

urlpatterns += [
    path('login/', login, name='login'),
    path('login/admin/', admin_login, name='admin_login'),
    path('activate-user/<int:user_id>/', activate_user, name='activate_user'),
    path('logout/', logout, name='logout'),
    path('access/', get_access_token, name='access'),
]
