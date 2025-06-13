from django.db import models
from documents.models import Document
from django.db import models

class Metadata(models.Model):
    """
    Métadonnées personnalisées pour les documents (spécifiques à l'archive).
    """
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='archive_metadata')  # Changé ici
    key = models.CharField(max_length=100)
    value_type = models.CharField(max_length=50)
    value_text = models.TextField()
    
    def __str__(self):
        return f"{self.document.title} - {self.key} (Archive)"

    class Meta:
        unique_together = ['document', 'key']