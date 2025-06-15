# ==========================================
# VERSIONS ULTRA-SIMPLIFIÉES POUR MYSQL
# ==========================================

# 1. documents/models.py - VERSION ULTRA-SIMPLE
from django.db import models
from users.models import User
from Catalog.models import Category
from django.utils import timezone

class DocumentType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    label = models.CharField(max_length=100)
    extensions = models.JSONField(default=list)
    mime_types = models.JSONField(default=list)
    
    def __str__(self):
        return self.label

class Document(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='documents')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_documents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    STATUS_CHOICES = [
        ('DRAFT', 'Brouillon'),
        ('PUBLISHED', 'Publié'),
        ('ARCHIVED', 'Archivé'),
        ('DELETED', 'Supprimé'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='DRAFT')
    is_favorite = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    file_hash = models.CharField(max_length=64, blank=True, null=True)
    
    # Fichier
    file_size = models.BigIntegerField(default=0)
    mime_type = models.CharField(max_length=100, blank=True)
    original_filename = models.CharField(max_length=255, blank=True)
    
    # Recently Accessed
    last_accessed = models.DateTimeField(null=True, blank=True)
    access_count = models.IntegerField(default=0)
    
    # Trash
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='deleted_documents')
    
    # OCR
    ocr_content = models.TextField(blank=True)
    ocr_processed = models.BooleanField(default=False)
    
    # Relations
    document_type = models.ForeignKey(DocumentType, on_delete=models.SET_NULL, null=True, blank=True)
    cabinet = models.ForeignKey('cabinets.Cabinet', on_delete=models.SET_NULL, null=True, blank=True)
    workflow_state = models.ForeignKey('workflows.WorkflowState', on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def mark_as_accessed(self, user=None):
        self.last_accessed = timezone.now()
        self.access_count += 1
        self.save()
        if user:
            DocumentAccess.objects.create(document=self, user=user)
    
    def soft_delete(self, user):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.deleted_by = user
        self.save()
    
    def restore_from_trash(self):
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        self.save()
    
    @property
    def can_be_restored(self):
        if not self.deleted_at:
            return False
        return (timezone.now() - self.deleted_at).days < 30

class DocumentVersion(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='versions')
    version_number = models.IntegerField()
    file_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_versions')
    comment = models.TextField(blank=True)

    class Meta:
        unique_together = ['document', 'version_number']

    def __str__(self):
        return f"{self.document.title} - v{self.version_number}"

class DocumentAccess(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='access_history')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accessed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.document.title}"

class Metadata(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='documents_metadata')
    key = models.CharField(max_length=100)
    value_type = models.CharField(max_length=50, choices=[
        ('text', 'Texte'),
        ('number', 'Nombre'),
        ('date', 'Date'),
        ('boolean', 'Booléen'),
    ], default='text')
    value_text = models.TextField()
    value_number = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    value_date = models.DateField(null=True, blank=True)
    value_boolean = models.BooleanField(null=True, blank=True)
    
    class Meta:
        unique_together = ['document', 'key']

    def __str__(self):
        return f"{self.document.title} - {self.key}"

class SearchIndex(models.Model):
    document = models.OneToOneField(Document, on_delete=models.CASCADE, related_name='search_index')
    content_text = models.TextField()
    metadata_text = models.TextField()
    indexed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Index de {self.document.title}"
