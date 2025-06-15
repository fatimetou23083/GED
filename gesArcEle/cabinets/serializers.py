# cabinets/serializers.py - النسخة الكاملة مع CabinetTreeSerializer
from rest_framework import serializers
from .models import Cabinet

class CabinetSerializer(serializers.ModelSerializer):
    """مسلسل للخزائن"""
    owner_name = serializers.SerializerMethodField()
    parent_name = serializers.SerializerMethodField()
    document_count = serializers.SerializerMethodField()
    has_children = serializers.SerializerMethodField()
    
    class Meta:
        model = Cabinet
        fields = [
            'id', 'name', 'description', 'parent', 'parent_name',
            'is_private', 'owner', 'owner_name', 'color', 'icon',
            'document_count', 'has_children', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'owner_name', 'parent_name', 
                           'document_count', 'has_children']
    
    def get_owner_name(self, obj):
        if obj.owner:
            return f"{obj.owner.first_name} {obj.owner.last_name}".strip() or obj.owner.username
        return None
    
    def get_parent_name(self, obj):
        return obj.parent.name if obj.parent else None
    
    def get_document_count(self, obj):
        try:
            from documents.models import Document
            return Document.objects.filter(cabinet=obj, is_deleted=False).count()
        except ImportError:
            return 0
    
    def get_has_children(self, obj):
        return Cabinet.objects.filter(parent=obj).exists()

class CabinetTreeSerializer(CabinetSerializer):
    """مسلسل لهيكل شجرة الخزائن"""
    children = serializers.SerializerMethodField()
    
    class Meta(CabinetSerializer.Meta):
        fields = CabinetSerializer.Meta.fields + ['children']
    
    def get_children(self, obj):
        """الحصول على الخزائن الفرعية مع إدارة الصلاحيات"""
        children = Cabinet.objects.filter(parent=obj)
        
        # تصفية حسب صلاحيات المستخدم
        request = self.context.get('request')
        if request and not request.user.is_staff:
            from django.db import models
            children = children.filter(
                models.Q(is_private=False) | 
                models.Q(owner=request.user)
            )
        
        serializer = CabinetTreeSerializer(
            children, 
            many=True, 
            context=self.context
        )
        return serializer.data

class CabinetMoveSerializer(serializers.Serializer):
    """مسلسل لنقل خزانة"""
    new_parent_id = serializers.IntegerField(required=False, allow_null=True)
    
    def validate_new_parent_id(self, value):
        if value is not None:
            try:
                Cabinet.objects.get(id=value)
            except Cabinet.DoesNotExist:
                raise serializers.ValidationError("الخزانة الأب غير موجودة")
        return value