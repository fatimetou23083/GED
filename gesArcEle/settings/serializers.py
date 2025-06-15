# settings/serializers.py
from rest_framework import serializers
from .models import SystemSettings, UserPreference, ApplicationSettings

class SystemSettingsSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les paramètres système"""
    updated_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = SystemSettings
        fields = [
            'id', 'site_name', 'site_description', 'logo_url',
            'max_file_size', 'allowed_file_types', 'max_files_per_upload',
            'ocr_enabled', 'ocr_language', 'ocr_auto_process',
            'trash_retention_days', 'auto_cleanup_enabled',
            'enable_full_text_search', 'search_results_per_page',
            'require_2fa', 'session_timeout_minutes', 'max_login_attempts',
            'email_notifications_enabled', 'smtp_server', 'smtp_port',
            'smtp_username', 'smtp_use_tls',
            'created_at', 'updated_at', 'updated_by_name'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'updated_by_name']
        extra_kwargs = {
            'smtp_password': {'write_only': True}
        }
    
    def get_updated_by_name(self, obj):
        if obj.updated_by:
            return f"{obj.updated_by.first_name} {obj.updated_by.last_name}".strip() or obj.updated_by.username
        return None

class UserPreferenceSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les préférences utilisateur"""
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = UserPreference
        fields = [
            'id', 'user_id', 'user_name',
            'theme', 'language', 'items_per_page', 'default_view',
            'email_notifications', 'desktop_notifications', 'notification_sound',
            'auto_save_favorites', 'show_hidden_files', 'default_sort_field', 'default_sort_order',
            'search_history_enabled', 'save_searches',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user_id', 'user_name', 'created_at', 'updated_at']
    
    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username

class ApplicationSettingsSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les paramètres d'application"""
    typed_value = serializers.SerializerMethodField()
    
    class Meta:
        model = ApplicationSettings
        fields = [
            'id', 'key', 'value', 'typed_value', 'data_type',
            'description', 'category', 'is_public',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'typed_value', 'created_at', 'updated_at']
    
    def get_typed_value(self, obj):
        """Retourner la valeur avec le bon type"""
        return obj.get_value()
    
    def validate_value(self, value):
        """Valider la valeur selon le type de données"""
        data_type = self.initial_data.get('data_type', 'string')
        
        if data_type == 'integer':
            try:
                int(value)
            except ValueError:
                raise serializers.ValidationError("La valeur doit être un entier")
        
        elif data_type == 'boolean':
            if str(value).lower() not in ('true', 'false', '1', '0', 'yes', 'no', 'on', 'off'):
                raise serializers.ValidationError("La valeur doit être un booléen")
        
        elif data_type == 'json':
            import json
            try:
                json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError("La valeur doit être un JSON valide")
        
        return value