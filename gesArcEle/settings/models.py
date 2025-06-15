# settings/models.py
from django.db import models
from users.models import User

class SystemSettings(models.Model):
    """Paramètres système globaux"""
    
    # Paramètres généraux
    site_name = models.CharField(max_length=100, default="GesArcEle")
    site_description = models.TextField(blank=True)
    logo_url = models.URLField(blank=True)
    
    # Paramètres de fichiers
    max_file_size = models.BigIntegerField(default=52428800)  # 50MB
    allowed_file_types = models.JSONField(default=list)
    max_files_per_upload = models.IntegerField(default=10)
    
    # Paramètres OCR
    ocr_enabled = models.BooleanField(default=True)
    ocr_language = models.CharField(max_length=10, default='fra')
    ocr_auto_process = models.BooleanField(default=True)
    
    # Paramètres de corbeille
    trash_retention_days = models.IntegerField(default=30)
    auto_cleanup_enabled = models.BooleanField(default=True)
    
    # Paramètres de recherche
    enable_full_text_search = models.BooleanField(default=True)
    search_results_per_page = models.IntegerField(default=25)
    
    # Paramètres de sécurité
    require_2fa = models.BooleanField(default=False)
    session_timeout_minutes = models.IntegerField(default=480)  # 8 heures
    max_login_attempts = models.IntegerField(default=5)
    
    # Paramètres de notifications
    email_notifications_enabled = models.BooleanField(default=True)
    smtp_server = models.CharField(max_length=100, blank=True)
    smtp_port = models.IntegerField(default=587)
    smtp_username = models.CharField(max_length=100, blank=True)
    smtp_password = models.CharField(max_length=100, blank=True)
    smtp_use_tls = models.BooleanField(default=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "Paramètres système"
        verbose_name_plural = "Paramètres système"
    
    def __str__(self):
        return f"Paramètres système - {self.site_name}"
    
    @classmethod
    def get_settings(cls):
        """Récupérer les paramètres système (singleton)"""
        settings, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'GesArcEle',
                'allowed_file_types': ['pdf', 'doc', 'docx', 'txt', 'jpg', 'png', 'gif']
            }
        )
        return settings

class UserPreference(models.Model):
    """Préférences utilisateur"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    
    # Préférences d'interface
    theme = models.CharField(max_length=20, choices=[
        ('light', 'Clair'),
        ('dark', 'Sombre'),
        ('auto', 'Automatique'),
    ], default='light')
    
    language = models.CharField(max_length=10, choices=[
        ('fr', 'Français'),
        ('en', 'English'),
        ('ar', 'العربية'),
    ], default='fr')
    
    items_per_page = models.IntegerField(default=25)
    default_view = models.CharField(max_length=20, choices=[
        ('list', 'Liste'),
        ('grid', 'Grille'),
        ('tiles', 'Tuiles'),
    ], default='list')
    
    # Préférences de notifications
    email_notifications = models.BooleanField(default=True)
    desktop_notifications = models.BooleanField(default=True)
    notification_sound = models.BooleanField(default=False)
    
    # Préférences de documents
    auto_save_favorites = models.BooleanField(default=True)
    show_hidden_files = models.BooleanField(default=False)
    default_sort_field = models.CharField(max_length=20, choices=[
        ('title', 'Titre'),
        ('created_at', 'Date de création'),
        ('updated_at', 'Date de modification'),
        ('file_size', 'Taille'),
    ], default='created_at')
    
    default_sort_order = models.CharField(max_length=10, choices=[
        ('asc', 'Croissant'),
        ('desc', 'Décroissant'),
    ], default='desc')
    
    # Préférences de recherche
    search_history_enabled = models.BooleanField(default=True)
    save_searches = models.BooleanField(default=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Préférences de {self.user.username}"

class ApplicationSettings(models.Model):
    """Paramètres d'application spécifiques"""
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    data_type = models.CharField(max_length=20, choices=[
        ('string', 'Chaîne'),
        ('integer', 'Entier'),
        ('boolean', 'Booléen'),
        ('json', 'JSON'),
    ], default='string')
    
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, default='general')
    is_public = models.BooleanField(default=False)  # Visible aux utilisateurs non-admin
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'key']
    
    def __str__(self):
        return f"{self.key} = {self.value}"
    
    def get_value(self):
        """Récupérer la valeur typée"""
        if self.data_type == 'integer':
            return int(self.value)
        elif self.data_type == 'boolean':
            return self.value.lower() in ('true', '1', 'yes', 'on')
        elif self.data_type == 'json':
            import json
            return json.loads(self.value)
        return self.value