from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tags', views.TagViewSet)
router.register(r'document-tags', views.DocumentTagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]