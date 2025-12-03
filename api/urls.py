from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import IdosoViewSet

router = DefaultRouter()
router.register(r'idosos', IdosoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]