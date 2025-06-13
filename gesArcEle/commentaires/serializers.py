from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les commentaires"""
    author_name = serializers.SerializerMethodField()
    has_replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'document_id', 'author_id', 'author_name', 'content', 
                 'created_at', 'parent_id', 'has_replies']
        read_only_fields = ['id', 'author_id', 'author_name', 'created_at', 'has_replies']
    
    def get_author_name(self, obj):
        if obj.author_id:
            return f"{obj.author_id.first_name} {obj.author_id.last_name}".strip() or obj.author_id.username
        return "Anonyme"
    
    def get_has_replies(self, obj):
        return Comment.objects.filter(parent_id=obj.id).exists()

class CommentCreateSerializer(serializers.ModelSerializer):
    """Sérialiseur pour créer des commentaires"""
    class Meta:
        model = Comment
        fields = ['document_id', 'content', 'parent_id']

class RecursiveField(serializers.Serializer):
    """Champ récursif pour les commentaires imbriqués"""
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class CommentTreeSerializer(CommentSerializer):
    """Sérialiseur pour l'arborescence de commentaires"""
    replies = RecursiveField(many=True, read_only=True)
    
    class Meta(CommentSerializer.Meta):
        fields = CommentSerializer.Meta.fields + ['replies']
    
    def get_fields(self):
        fields = super().get_fields()
        fields['replies'] = serializers.SerializerMethodField()
        return fields
    
    def get_replies(self, obj):
        replies = Comment.objects.filter(parent_id=obj.id)
        serializer = CommentTreeSerializer(replies, many=True, context=self.context)
        return serializer.data