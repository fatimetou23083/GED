from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Modèle utilisateur étendu à partir du modèle AbstractUser de Django.
    """
    # Redéfinir ces champs avec des related_name uniques
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_permissions'
    )

    def __str__(self):
        return self.username


class Profile(models.Model):
    """
    Profil utilisateur avec des informations supplémentaires.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"Profil de {self.user.username}"