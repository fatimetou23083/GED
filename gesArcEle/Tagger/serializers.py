from rest_framework import serializers
from .models import Tag, DocumentTag

class TagSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les tags"""
    document_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'document_count']
        read_only_fields = ['id', 'document_count']
    
    def get_document_count(self, obj):
        return DocumentTag.objects.filter(tag_id=obj.id).count()

class DocumentTagSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les associations document-tag"""
    tag_name = serializers.SerializerMethodField()
    tag_color = serializers.SerializerMethodField()
    
    class Meta:
        model = DocumentTag
        fields = ['id', 'document_id', 'tag_id', 'tag_name', 'tag_color']
        read_only_fields = ['id', 'tag_name', 'tag_color']
    
    def get_tag_name(self, obj):
        return obj.tag_id.name if obj.tag_id else ""
    
    def get_tag_color(self, obj):
        return obj.tag_id.color if obj.tag_id else ""