# settings/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'system', views.SystemSettingsViewSet, basename='system-settings')
router.register(r'preferences', views.UserPreferenceViewSet)
router.register(r'application', views.ApplicationSettingsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('system/current/', views.SystemSettingsViewSet.as_view({'get': 'current'}), name='current-settings'),
    path('preferences/my/', views.UserPreferenceViewSet.as_view({'get': 'my_preferences', 'put': 'my_preferences'}), name='my-preferences'),
    path('application/public/', views.ApplicationSettingsViewSet.as_view({'get': 'public_settings'}), name='public-settings'),
]