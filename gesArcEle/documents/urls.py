from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import DocumentViewSet

router = DefaultRouter()

router.register(r'versions', views.DocumentVersionViewSet)
router.register(r'metadata', views.MetadataViewSet)
router.register(r'documents', DocumentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]