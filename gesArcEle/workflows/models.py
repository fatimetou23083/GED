# workflows/models.py
from django.db import models
from users.models import User

class WorkflowDefinition(models.Model):
    """Définition de workflow"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class WorkflowState(models.Model):
    """États du workflow"""
    workflow = models.ForeignKey(WorkflowDefinition, on_delete=models.CASCADE, related_name='states')
    name = models.CharField(max_length=100)
    label = models.CharField(max_length=100)
    is_initial = models.BooleanField(default=False)
    is_final = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['workflow', 'name']
    
    def __str__(self):
        return f"{self.workflow.name} - {self.label}"