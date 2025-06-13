from django.utils import timezone
from rest_framework import serializers
from .models import Permission

class PermissionSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les permissions"""
    user_name = serializers.SerializerMethodField()
    document_title = serializers.SerializerMethodField()
    
    class Meta:
        model = Permission
        fields = ['id', 'document_id', 'document_title', 'user_id', 'user_name', 
                 'permission_type', 'granted_at']
        read_only_fields = ['id', 'granted_at', 'user_name', 'document_title']
    
    def get_user_name(self, obj):
        if obj.user_id:
            return f"{obj.user_id.first_name} {obj.user_id.last_name}".strip() or obj.user_id.username
        return ""
    
    def get_document_title(self, obj):
        return obj.document_id.title if obj.document_id else ""
    
    def create(self, validated_data):
        # Ajoute automatiquement la date d'attribution
        validated_data['granted_at'] = timezone.now()
        return super().create(validated_data)