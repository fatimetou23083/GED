# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'profiles', views.ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', views.UserViewSet.as_view({'post': 'register'}), name='user-register'),
    path('auth/login/', views.UserViewSet.as_view({'post': 'login'}), name='user-login'),
    
    # Nouveaux endpoints pour la liste des utilisateurs
    path('users/list_with_profiles/', views.UserViewSet.as_view({'get': 'list_with_profiles'}), name='users-with-profiles'),
    path('users/search/', views.UserViewSet.as_view({'get': 'search'}), name='users-search'),
    path('users/stats/', views.UserViewSet.as_view({'get': 'stats'}), name='users-stats'),
]
