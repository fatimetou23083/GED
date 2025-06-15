# Tagger/serializers.py
from rest_framework import serializers
from .models import Tag, DocumentTag

class TagSerializer(serializers.ModelSerializer):
    usage_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'usage_count']
        read_only_fields = ['id', 'usage_count']
    
    def get_usage_count(self, obj):
        return DocumentTag.objects.filter(tag=obj).count()

class DocumentTagSerializer(serializers.ModelSerializer):
    tag_name = serializers.SerializerMethodField()
    tag_color = serializers.SerializerMethodField()
    
    class Meta:
        model = DocumentTag
        fields = ['id', 'document_id', 'tag_id', 'tag_name', 'tag_color']
        read_only_fields = ['id', 'tag_name', 'tag_color']
    
    def get_tag_name(self, obj):
        return obj.tag.name if obj.tag else ""
    
    def get_tag_color(self, obj):
        return obj.tag.color if obj.tag else ""