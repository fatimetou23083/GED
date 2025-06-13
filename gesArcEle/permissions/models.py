from django.db import models
from documents.models import Document
from users.models import User

class Permission(models.Model):
    PERMISSION_TYPES = (
        ('READ', 'Lecture'),
        ('WRITE', 'Écriture'),
        ('DELETE', 'Suppression'),
        ('ADMIN', 'Administration'),
    )

    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='permissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='document_permissions')
    permission_type = models.CharField(max_length=10, choices=PERMISSION_TYPES)
    granted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['document', 'user', 'permission_type']

    def __str__(self):
        return f"{self.user.username} - {self.permission_type} - {self.document.title}"
