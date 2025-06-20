# Catalog/serializers.py - VERSION COMPLÈTE
from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    """Sérialiseur pour les catégories"""
    parent_name = serializers.SerializerMethodField()
    document_count = serializers.SerializerMethodField()
    has_children = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent', 'parent_name', 
                 'document_count', 'has_children']
        read_only_fields = ['id', 'parent_name', 'document_count', 'has_children']
    
    def get_parent_name(self, obj):
        return obj.parent.name if obj.parent else ""
    
    def get_document_count(self, obj):
        try:
            from documents.models import Document
            return Document.objects.filter(category=obj).count()
        except ImportError:
            return 0
    
    def get_has_children(self, obj):
        return Category.objects.filter(parent=obj).exists()

class RecursiveCategoryField(serializers.Serializer):
    """Champ récursif pour l'arborescence des catégories"""
    def to_representation(self, value):
        serializer = CategoryTreeSerializer(value, context=self.context)
        return serializer.data

class CategoryTreeSerializer(CategorySerializer):
    """Sérialiseur pour l'arborescence des catégories"""
    children = serializers.SerializerMethodField()
    
    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + ['children']
    
    def get_children(self, obj):
        children = Category.objects.filter(parent=obj)
        serializer = CategoryTreeSerializer(children, many=True, context=self.context)
        return serializer.data