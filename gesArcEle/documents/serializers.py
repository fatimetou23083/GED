# documents/serializers.py - VERSION CORRIGÉE
from rest_framework import serializers
from django.conf import settings
import os

# Imports des modèles locaux
from .models import Document, DocumentVersion, DocumentAccess, Metadata, SearchIndex, DocumentType

# Imports des modèles d'autres apps
from users.models import User
from Catalog.models import Category
from users.serializers import UserSerializer

class DocumentTypeSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les types de documents"""
    
    class Meta:
        model = DocumentType
        fields = ['id', 'name', 'label', 'extensions', 'mime_types']
        read_only_fields = ['id']

class DocumentVersionSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les versions de documents"""
    created_by_name = serializers.SerializerMethodField()
    file_size = serializers.SerializerMethodField()
    
    class Meta:
        model = DocumentVersion
        fields = [
            'id', 'document_id', 'version_number', 'file_path', 
            'created_at', 'created_by_id', 'created_by_name', 'comment', 'file_size'
        ]
        read_only_fields = ['id', 'created_at', 'created_by_name', 'file_size']
    
    def get_created_by_name(self, obj):
        return f"{obj.created_by.first_name} {obj.created_by.last_name}".strip() or obj.created_by.username
    
    def get_file_size(self, obj):
        try:
            file_path = os.path.join(settings.MEDIA_ROOT, obj.file_path)
            return os.path.getsize(file_path)
        except (OSError, AttributeError):
            return 0

class MetadataSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les métadonnées"""
    
    class Meta:
        model = Metadata
        fields = [
            'id', 'document_id', 'key', 'value_type', 'value_text',
            'value_number', 'value_date', 'value_boolean'
        ]
        read_only_fields = ['id']

# Import pour éviter l'erreur circulaire
try:
    from Catalog.serializers import CategorySerializer
except ImportError:
    # Fallback si CategorySerializer n'existe pas encore
    class CategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = Category
            fields = ['id', 'name', 'description']

class DocumentSerializer(serializers.ModelSerializer):
    """Sérialiseur principal pour les documents"""
    creator = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True,
        source='category'
    )
    file = serializers.FileField(write_only=True, required=False)
    file_size_formatted = serializers.SerializerMethodField()
    file_type = serializers.SerializerMethodField()
    last_version = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = [
            'id', 'title', 'description', 'category', 'category_id',
            'creator', 'created_at', 'updated_at', 'status',
            'is_favorite', 'is_deleted', 'file_hash', 'file_size',
            'file_size_formatted', 'mime_type', 'original_filename',
            'last_accessed', 'access_count', 'ocr_content', 'ocr_processed',
            'document_type', 'cabinet', 'workflow_state', 'file', 'file_type', 'last_version'
        ]
        read_only_fields = [
            'id', 'creator', 'created_at', 'updated_at', 'file_hash',
            'file_size', 'file_size_formatted', 'mime_type', 'last_accessed',
            'access_count', 'ocr_processed', 'file_type', 'last_version'
        ]
    
    def get_file_size_formatted(self, obj):
        """Formatter la taille du fichier"""
        size = obj.file_size
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        elif size < 1024 * 1024 * 1024:
            return f"{size / (1024 * 1024):.1f} MB"
        else:
            return f"{size / (1024 * 1024 * 1024):.1f} GB"
    
    def get_file_type(self, obj):
        """Récupérer l'extension du fichier"""
        if obj.original_filename:
            return os.path.splitext(obj.original_filename)[1][1:].lower()
        return ''
    
    def get_last_version(self, obj):
        """Récupérer la dernière version"""
        try:
            latest_version = obj.versions.latest('version_number')
            return {
                'version_number': latest_version.version_number,
                'created_at': latest_version.created_at,
                'created_by': latest_version.created_by.username
            }
        except DocumentVersion.DoesNotExist:
            return None

class DocumentDetailSerializer(DocumentSerializer):
    """Sérialiseur détaillé pour les documents"""
    versions = DocumentVersionSerializer(many=True, read_only=True)
    metadata = MetadataSerializer(source='documents_metadata', many=True, read_only=True)
    tags = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    
    class Meta(DocumentSerializer.Meta):
        fields = DocumentSerializer.Meta.fields + ['versions', 'metadata', 'tags', 'permissions']
    
    def get_tags(self, obj):
        """Récupérer les tags du document"""
        try:
            from Tagger.models import Tag
            tags = Tag.objects.filter(documenttag__document=obj)
            return [{'id': tag.id, 'name': tag.name, 'color': tag.color} for tag in tags]
        except ImportError:
            return []
    
    def get_permissions(self, obj):
        """Récupérer les permissions du document"""
        try:
            from permissions.models import Permission
            permissions = Permission.objects.filter(document=obj)
            return [{
                'user_id': perm.user.id,
                'user_name': perm.user.username,
                'permission_type': perm.permission_type
            } for perm in permissions]
        except ImportError:
            return []

class DocumentCreateSerializer(serializers.ModelSerializer):
    """Sérialiseur pour créer des documents"""
    file = serializers.FileField(required=True)
    
    class Meta:
        model = Document
        fields = ['title', 'description', 'category', 'file']
    
    def create(self, validated_data):
        """Créer un document avec fichier"""
        file_obj = validated_data.pop('file')
        document = Document.objects.create(**validated_data)
        
        # Traiter le fichier...
        # (La logique de traitement du fichier sera dans la vue)
        
        return document