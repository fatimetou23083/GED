# workflows/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'definitions', views.WorkflowDefinitionViewSet)
router.register(r'states', views.WorkflowStateViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('definitions/<int:pk>/assign/', views.WorkflowDefinitionViewSet.as_view({'post': 'assign_to_document'}), name='assign-workflow'),
    path('definitions/<int:pk>/states/', views.WorkflowDefinitionViewSet.as_view({'get': 'get_states'}), name='workflow-states'),
]