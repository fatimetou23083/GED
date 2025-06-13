from django.db import models

class Category(models.Model):
    """
    Catégorie de documents avec possibilité de hiérarchie (catégories parent-enfant).
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'
