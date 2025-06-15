# messaging/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'messages', views.MessageViewSet)
router.register(r'notifications', views.NotificationViewSet)
router.register(r'templates', views.MessageTemplateViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('messages/unread-count/', views.MessageViewSet.as_view({'get': 'unread_count'}), name='unread-count'),
    path('messages/mark-all-read/', views.MessageViewSet.as_view({'post': 'mark_all_read'}), name='mark-all-read'),
    path('notifications/broadcast/', views.NotificationViewSet.as_view({'post': 'broadcast'}), name='broadcast-notification'),
]