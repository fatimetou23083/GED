# indexing/models.py
from django.db import models
from documents.models import Document
from users.models import User

class IndexQueue(models.Model):
    """File d'attente pour l'indexation"""
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('PROCESSING', 'En cours'),
        ('COMPLETED', 'Terminé'),
        ('FAILED', 'Échoué'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    retry_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Indexation {self.document.title} - {self.status}"

class IndexingJob(models.Model):
    """Jobs d'indexation"""
    JOB_TYPES = [
        ('OCR', 'OCR'),
        ('THUMBNAIL', 'Miniature'),
        ('METADATA', 'Métadonnées'),
        ('FULL_TEXT', 'Texte intégral'),
    ]
    
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    status = models.CharField(max_length=20, choices=IndexQueue.STATUS_CHOICES, default='PENDING')
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    result_data = models.JSONField(default=dict, blank=True)
    error_message = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['document', 'job_type']
    
    def __str__(self):
        return f"{self.job_type} - {self.document.title}"

class IndexingStats(models.Model):
    """Statistiques d'indexation"""
    date = models.DateField(auto_now_add=True)
    total_documents = models.IntegerField(default=0)
    indexed_documents = models.IntegerField(default=0)
    failed_documents = models.IntegerField(default=0)
    processing_time_avg = models.FloatField(default=0.0)
    
    class Meta:
        unique_together = ['date']
        ordering = ['-date']
    
    def __str__(self):
        return f"Stats {self.date}"