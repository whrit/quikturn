from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, LogoViewSet

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'logos', LogoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]