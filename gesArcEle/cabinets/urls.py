# cabinets/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'cabinets', views.CabinetViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('cabinets/tree/', views.CabinetViewSet.as_view({'get': 'tree'}), name='cabinets-tree'),
    path('cabinets/<int:pk>/documents/', views.CabinetViewSet.as_view({'get': 'documents'}), name='cabinet-documents'),
    path('cabinets/<int:pk>/move/', views.CabinetViewSet.as_view({'post': 'move'}), name='cabinet-move'),
]