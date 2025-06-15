# cabinets/models.py
from django.db import models
from users.models import User

class Cabinet(models.Model):
    """Système de classeurs Mayan"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    
    # Fonctionnalités étendues
    is_private = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    color = models.CharField(max_length=7, default='#1976D2')
    icon = models.CharField(max_length=50, default='folder')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name