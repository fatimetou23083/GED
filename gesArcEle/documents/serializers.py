# documents/serializers.py - VERSION CORRIGÉE
from rest_framework import serializers
from .models import Document, DocumentVersion, Metadata

class DocumentSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les documents"""
    creator_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = [
            'id', 'title', 'description',
            'category_id', 'category_name',
            'creator_id', 'creator_name',
            'created_at', 'updated_at', 'status',
            'is_favorite', 'is_deleted', 'file_hash'
        ]
        read_only_fields = [
            'id', 'creator_id', 'creator_name',
            'created_at', 'updated_at', 'file_hash'
        ]

    def get_creator_name(self, obj):
        if obj.creator:
            full_name = f"{obj.creator.first_name} {obj.creator.last_name}".strip()
            return full_name if full_name else obj.creator.username
        return ""

    def get_category_name(self, obj):
        return obj.category.name if obj.category else ""


class DocumentVersionSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les versions de documents"""
    creator_name = serializers.SerializerMethodField()
    
    class Meta:
        model = DocumentVersion
        fields = ['id', 'document_id', 'version_number', 'file_path', 
                 'created_at', 'created_by_id', 'creator_name']
        read_only_fields = ['id', 'version_number', 'created_at', 'created_by_id', 'creator_name']
    
    def get_creator_name(self, obj):
        if obj.created_by:
            full_name = f"{obj.created_by.first_name} {obj.created_by.last_name}".strip()
            return full_name if full_name else obj.created_by.username
        return ""


class MetadataSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les métadonnées"""
    class Meta:
        model = Metadata
        fields = ['id', 'document_id', 'key', 'value_type', 'value_text']
        read_only_fields = ['id']


class DocumentDetailSerializer(DocumentSerializer):
    """Sérialiseur pour les détails d'un document"""
    versions = DocumentVersionSerializer(many=True, read_only=True)
    metadata = MetadataSerializer(source='documents_metadata', many=True, read_only=True)
    
    class Meta(DocumentSerializer.Meta):
        fields = DocumentSerializer.Meta.fields + ['versions', 'metadata']