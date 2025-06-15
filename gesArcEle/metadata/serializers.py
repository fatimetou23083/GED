# metadata/serializers.py
from rest_framework import serializers
from .models import MetadataType

class MetadataTypeSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les types de métadonnées"""
    usage_count = serializers.SerializerMethodField()
    
    class Meta:
        model = MetadataType
        fields = [
            'id', 'name', 'label', 'data_type', 'required', 
            'choices', 'usage_count'
        ]
        read_only_fields = ['id', 'usage_count']
    
    def get_usage_count(self, obj):
        """Compter combien de fois ce type de métadonnée est utilisé"""
        from documents.models import Metadata
        return Metadata.objects.filter(key=obj.name).count()
    
    def validate_name(self, value):
        """Valider le nom (doit être unique et format correct)"""
        import re
        
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', value):
            raise serializers.ValidationError(
                "Le nom doit commencer par une lettre et ne contenir que des lettres, chiffres et underscores"
            )
        
        return value
    
    def validate_choices(self, value):
        """Valider les choix pour le type 'choice'"""
        data_type = self.initial_data.get('data_type')
        
        if data_type == 'choice':
            if not value or not isinstance(value, list):
                raise serializers.ValidationError(
                    "Les choix sont requis pour le type 'choice' et doivent être une liste"
                )
            
            if len(value) < 2:
                raise serializers.ValidationError(
                    "Au moins 2 choix sont requis pour le type 'choice'"
                )
        
        return value

class MetadataValueSerializer(serializers.Serializer):
    """Sérialiseur pour les valeurs de métadonnées"""
    document_id = serializers.IntegerField()
    metadata_type_id = serializers.IntegerField()
    value = serializers.CharField()
    
    def validate(self, data):
        """Valider les données selon le type de métadonnée"""
        try:
            metadata_type = MetadataType.objects.get(id=data['metadata_type_id'])
        except MetadataType.DoesNotExist:
            raise serializers.ValidationError("Type de métadonnée introuvable")
        
        value = data['value']
        
        # Validation selon le type de données
        if metadata_type.data_type == 'number':
            try:
                float(value)
            except ValueError:
                raise serializers.ValidationError("La valeur doit être un nombre")
        
        elif metadata_type.data_type == 'date':
            from datetime import datetime
            try:
                datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                raise serializers.ValidationError("La valeur doit être une date au format YYYY-MM-DD")
        
        elif metadata_type.data_type == 'boolean':
            if value.lower() not in ['true', 'false', '1', '0', 'yes', 'no']:
                raise serializers.ValidationError("La valeur doit être un booléen")
        
        elif metadata_type.data_type == 'choice':
            if value not in metadata_type.choices:
                raise serializers.ValidationError(f"La valeur doit être parmi: {', '.join(metadata_type.choices)}")
        
        return data