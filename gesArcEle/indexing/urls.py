# indexing/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'queue', views.IndexQueueViewSet)
router.register(r'jobs', views.IndexingJobViewSet)
router.register(r'stats', views.IndexingStatsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('reindex-all/', views.reindex_all_documents, name='reindex-all'),
    path('process-queue/', views.process_indexing_queue, name='process-queue'),
]