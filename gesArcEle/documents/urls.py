# documents/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'documents', views.DocumentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # URLs spécifiques pour les documents
    path('documents/all/', views.DocumentViewSet.as_view({'get': 'all_documents'}), name='all-documents'),
    path('documents/recent/', views.DocumentViewSet.as_view({'get': 'recently_accessed'}), name='recent-documents'),
    path('documents/created/', views.DocumentViewSet.as_view({'get': 'recently_created'}), name='recently-created'),
    path('documents/favorites/', views.DocumentViewSet.as_view({'get': 'favorites'}), name='favorite-documents'),
    path('documents/trash/', views.DocumentViewSet.as_view({'get': 'trash'}), name='trash-documents'),
    path('documents/search/', views.DocumentViewSet.as_view({'get': 'search'}), name='search-documents'),
    
    # Actions sur documents spécifiques
    path('documents/<int:pk>/toggle-favorite/', views.DocumentViewSet.as_view({'post': 'toggle_favorite'}), name='toggle-favorite'),
    path('documents/<int:pk>/soft-delete/', views.DocumentViewSet.as_view({'post': 'soft_delete'}), name='soft-delete'),
    path('documents/<int:pk>/restore/', views.DocumentViewSet.as_view({'post': 'restore'}), name='restore-document'),
    path('documents/<int:pk>/download/', views.DocumentViewSet.as_view({'get': 'download'}), name='download-document'),
    
    # API pour les statistiques
    path('dashboard-stats/', views.dashboard_stats, name='dashboard-stats'),
]