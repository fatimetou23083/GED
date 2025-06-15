# ==============================================================================
# messaging/serializers.py
from rest_framework import serializers
from .models import Message, Notification, MessageTemplate

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    recipient_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = ['id', 'title', 'content', 'message_type', 'recipient_id', 
                 'recipient_name', 'sender_id', 'sender_name', 'related_document_id',
                 'is_read', 'read_at', 'created_at', 'extra_data']
        read_only_fields = ['id', 'sender_id', 'created_at', 'sender_name', 'recipient_name']
    
    def get_sender_name(self, obj):
        if obj.sender:
            return f"{obj.sender.first_name} {obj.sender.last_name}".strip() or obj.sender.username
        return "النظام"
    
    def get_recipient_name(self, obj):
        return f"{obj.recipient.first_name} {obj.recipient.last_name}".strip() or obj.recipient.username

class NotificationSerializer(serializers.ModelSerializer):
    recipients_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = ['id', 'notification_type', 'title', 'message', 'recipients_count',
                 'related_document_id', 'created_at', 'expires_at', 'is_system', 
                 'action_url', 'action_label']
        read_only_fields = ['id', 'created_at', 'recipients_count']
    
    def get_recipients_count(self, obj):
        return obj.recipients.count()

class MessageTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageTemplate
        fields = ['id', 'name', 'subject_template', 'body_template', 'message_type',
                 'available_variables', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']
