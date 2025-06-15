# permissions/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'permissions', views.DocumentPermissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('permissions/check/', views.DocumentPermissionViewSet.as_view({'get': 'check'}), name='check-permission'),
    path('permissions/bulk-assign/', views.DocumentPermissionViewSet.as_view({'post': 'bulk_assign'}), name='bulk-assign-permissions'),
]