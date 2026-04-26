from rest_framework.routers import DefaultRouter
from .views import ContactViewSet, UsersViewSet, NewsViewSet, ExhibitionViewSet, ProductViewSet

router = DefaultRouter()

router.register(r'contact', ContactViewSet, basename='contact')
router.register(r'users', UsersViewSet, basename='users')
router.register(r'news', NewsViewSet, basename="news")
router.register(r'exhibitions', ExhibitionViewSet, basename="exhibitions")
router.register(r'products', ProductViewSet, basename="products")

urlpatterns = router.urls