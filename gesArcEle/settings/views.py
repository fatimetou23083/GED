# 🔧 إصلاح جميع ViewSets - المشكلة الأساسية: عدم وجود queryset

# 1. settings/views.py - النسخة المُصححة
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import SystemSettings, UserPreference, ApplicationSettings
from .serializers import SystemSettingsSerializer, UserPreferenceSerializer, ApplicationSettingsSerializer

class SystemSettingsViewSet(viewsets.ModelViewSet):
    queryset = SystemSettings.objects.all()  # إضافة queryset
    serializer_class = SystemSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
    
    @action(detail=False, methods=['GET'])
    def current(self, request):
        settings = SystemSettings.get_settings()
        serializer = self.get_serializer(settings)
        return Response(serializer.data)

class UserPreferenceViewSet(viewsets.ModelViewSet):
    queryset = UserPreference.objects.all()  # إضافة queryset
    serializer_class = UserPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """تصفية للمستخدم الحالي"""
        if self.request.user.is_staff:
            return UserPreference.objects.all()
        return UserPreference.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['GET', 'PUT', 'PATCH'])
    def my_preferences(self, request):
        try:
            preferences = UserPreference.objects.get(user=request.user)
            if request.method == 'GET':
                serializer = self.get_serializer(preferences)
                return Response(serializer.data)
            # للتحديث
            serializer = self.get_serializer(preferences, data=request.data, partial=request.method=='PATCH')
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserPreference.DoesNotExist:
            if request.method == 'GET':
                preferences = UserPreference.objects.create(user=request.user)
                serializer = self.get_serializer(preferences)
                return Response(serializer.data)
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApplicationSettingsViewSet(viewsets.ModelViewSet):
    queryset = ApplicationSettings.objects.all()  # إضافة queryset
    serializer_class = ApplicationSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

# ------------------------------------------------------------------
