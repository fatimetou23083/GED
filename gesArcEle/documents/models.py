# documents/models.py - VERSION CORRIGÉE
from django.db import models
from users.models import User
from Catalog.models import Category
from django.core.files.storage import default_storage
import hashlib

class Document(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='documents')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_documents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    status = models.CharField(max_length=50, default='DRAFT')
    
    # ✅ Nouveaux champs fonctionnels
    is_favorite = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    file_hash = models.CharField(max_length=64, blank=True, null=True)

    def save(self, *args, **kwargs):
        # ✅ Calcul automatique du hash SHA256 du fichier de la dernière version
        super().save(*args, **kwargs)  # Sauvegarder d'abord
        
        # Puis calculer le hash si une version existe
        latest_version = self.versions.order_by('-version_number').first()
        if latest_version and latest_version.file_path:
            try:
                with default_storage.open(latest_version.file_path, 'rb') as f:
                    file_content = f.read()
                    new_hash = hashlib.sha256(file_content).hexdigest()
                    if self.file_hash != new_hash:
                        self.file_hash = new_hash
                        # Éviter la récursion en utilisant update
                        Document.objects.filter(pk=self.pk).update(file_hash=new_hash)
            except Exception as e:
                # Logger l'erreur ou ignorer silencieusement
                print(f"Erreur lors du calcul du hash: {e}")

    def __str__(self):
        return self.title


class DocumentVersion(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='versions')
    version_number = models.IntegerField()
    file_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_versions')

    class Meta:
        unique_together = ['document', 'version_number']
        ordering = ['-version_number']

    def __str__(self):
        return f"{self.document.title} - v{self.version_number}"

    def save(self, *args, **kwargs):
        # Auto-incrémenter le numéro de version si pas défini
        if not self.version_number:
            last_version = DocumentVersion.objects.filter(document=self.document).order_by('-version_number').first()
            self.version_number = (last_version.version_number + 1) if last_version else 1
        
        super().save(*args, **kwargs)
        
        # Recalculer le hash du document parent
        self.document.save()


class Metadata(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='documents_metadata')
    key = models.CharField(max_length=100)
    value_type = models.CharField(max_length=50)
    value_text = models.TextField()

    class Meta:
        unique_together = ['document', 'key']

    def __str__(self):
        return f"{self.document.title} - {self.key}"


class SearchIndex(models.Model):
    document = models.OneToOneField(Document, on_delete=models.CASCADE, related_name='search_index')
    content_text = models.TextField()
    metadata_text = models.TextField()

    def __str__(self):
        return f"Index de {self.document.title}"