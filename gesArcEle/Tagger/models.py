from django.db import models
from documents.models import Document

class Tag(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class DocumentTag(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='document_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tag_documents')

    class Meta:
        unique_together = ['document', 'tag']

    def __str__(self):
        return f"{self.document.title} - {self.tag.name}"
