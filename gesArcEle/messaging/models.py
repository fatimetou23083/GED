
# ==========================================
# 2. messaging/models.py - VERSION SIMPLE
from django.db import models
from users.models import User
from documents.models import Document

class Message(models.Model):
    MESSAGE_TYPES = [
        ('INFO', 'Information'),
        ('WARNING', 'Avertissement'),
        ('ERROR', 'Erreur'),
        ('SUCCESS', 'Succès'),
        ('NOTIFICATION', 'Notification'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='INFO')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', null=True, blank=True)
    related_document = models.ForeignKey(Document, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    extra_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.title} - {self.recipient.username}"

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('DOCUMENT_SHARED', 'Document partagé'),
        ('DOCUMENT_COMMENTED', 'Document commenté'),
        ('WORKFLOW_CHANGED', 'Workflow modifié'),
        ('PERMISSION_GRANTED', 'Permission accordée'),
        ('SYSTEM_MAINTENANCE', 'Maintenance système'),
        ('QUOTA_WARNING', 'Avertissement quota'),
    ]
    
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    recipients = models.ManyToManyField(User, through='NotificationRecipient')
    related_document = models.ForeignKey(Document, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_system = models.BooleanField(default=False)
    action_url = models.URLField(blank=True)
    action_label = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.title} ({self.notification_type})"

class NotificationRecipient(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['notification', 'user']

    def __str__(self):
        return f"{self.notification.title} -> {self.user.username}"

class MessageTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subject_template = models.CharField(max_length=200)
    body_template = models.TextField()
    message_type = models.CharField(max_length=20, choices=Message.MESSAGE_TYPES, default='INFO')
    available_variables = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name