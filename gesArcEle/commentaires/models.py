from django.db import models
from documents.models import Document
from users.models import User

class Comment(models.Model):
    """
    Commentaires sur les documents avec possibilité de réponses hiérarchiques.
    """
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies')
    
    def __str__(self):
        return f"Commentaire de {self.author.username} sur {self.document.title}"