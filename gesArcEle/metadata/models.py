# metadata/models.py  
from django.db import models

class MetadataType(models.Model):
    """Types de métadonnées configurables"""
    name = models.CharField(max_length=100, unique=True)
    label = models.CharField(max_length=100)
    data_type = models.CharField(max_length=20, choices=[
        ('text', 'Texte'),
        ('number', 'Nombre'),
        ('date', 'Date'),
        ('boolean', 'Booléen'),
        ('choice', 'Choix'),
    ], default='text')
    
    required = models.BooleanField(default=False)
    choices = models.JSONField(default=list, blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.label