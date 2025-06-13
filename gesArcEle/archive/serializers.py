# archive/serializers.py
from rest_framework import serializers
# Changez cette ligne
# from .models import Category, Document, SearchIndex
# Par celle-ci
from Catalog.models import Category
from documents.models import Document, SearchIndex, DocumentVersion, Metadata
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CategorySerializer(serializers.ModelSerializer):
    """Sérialiseur pour les catégories d'archives"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent']

class DocumentSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True,
        source='category'
    )
    file = serializers.FileField(write_only=True, required=False)
    file_size = serializers.SerializerMethodField()
    file_type = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = [
            'id', 'title', 'description', 'category', 'category_id',
            'creator', 'created_at', 'status', 'file', 'file_size',
            'file_type'
        ]
        read_only_fields = ['creator', 'created_at', 'file_size', 'file_type']

    def get_file_size(self, obj):
        try:
            latest_version = obj.versions.latest('version_number')
            import os
            return os.path.getsize(latest_version.file_path)
        except (DocumentVersion.DoesNotExist, OSError):
            return 0

    def get_file_type(self, obj):
        try:
            latest_version = obj.versions.latest('version_number')
            import os
            return os.path.splitext(latest_version.file_path)[1][1:].lower()
        except DocumentVersion.DoesNotExist:
            return ''

    def create(self, validated_data):
        file = validated_data.pop('file', None)
        document = Document.objects.create(**validated_data)

        if file:
            version = DocumentVersion.objects.create(
                document=document,
                version_number=1,
                file_path=self._save_file(file, document),
                created_by=validated_data['creator']
            )

        return document

    def update(self, instance, validated_data):
        file = validated_data.pop('file', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if file:
            latest_version = instance.versions.latest('version_number')
            version = DocumentVersion.objects.create(
                document=instance,
                version_number=latest_version.version_number + 1,
                file_path=self._save_file(file, instance),
                created_by=instance.creator
            )

        return instance

    def _save_file(self, file, document):
        import os
        from django.conf import settings
        
        # Créer le chemin du fichier
        file_ext = os.path.splitext(file.name)[1]
        filename = f"document_{document.id}_v{document.versions.count() + 1}{file_ext}"
        relative_path = os.path.join('documents', str(document.id), filename)
        absolute_path = os.path.join(settings.MEDIA_ROOT, relative_path)
        
        # Créer le répertoire si nécessaire
        os.makedirs(os.path.dirname(absolute_path), exist_ok=True)
        
        # Sauvegarder le fichier
        with open(absolute_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        return relative_path

class DocumentDetailSerializer(DocumentSerializer):
    """Sérialiseur pour les détails d'un document d'archives"""
    # Ajoute des champs supplémentaires pour la vue détaillée
    versions = serializers.SerializerMethodField()
    metadata = serializers.SerializerMethodField()
    
    class Meta(DocumentSerializer.Meta):
        fields = DocumentSerializer.Meta.fields + ['versions', 'metadata']
    
    def get_versions(self, obj):
        return [{
            'version_number': version.version_number,
            'created_at': version.created_at,
            'created_by': UserSerializer(version.created_by).data,
            'file_path': version.file_path
        } for version in obj.versions.all()]
    
    def get_metadata(self, obj):
        return [{
            'key': meta.key,
            'value_type': meta.value_type,
            'value': meta.value_text
        } for meta in obj.documents_metadata.all()]