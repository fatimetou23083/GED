# metadata/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'types', views.MetadataTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('types/<int:pk>/assign/', views.MetadataTypeViewSet.as_view({'post': 'assign_to_document'}), name='assign-metadata'),
    path('types/bulk-create/', views.MetadataTypeViewSet.as_view({'post': 'bulk_create'}), name='bulk-create-metadata-types'),
]