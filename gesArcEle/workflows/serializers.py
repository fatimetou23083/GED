# workflows/serializers.py - النسخة الصحيحة النهائية
from rest_framework import serializers
from .models import WorkflowDefinition, WorkflowState

class WorkflowStateSerializer(serializers.ModelSerializer):
    """مسلسل لحالات سير العمل"""
    
    class Meta:
        model = WorkflowState
        fields = ['id', 'workflow', 'name', 'label', 'is_initial', 'is_final']
        read_only_fields = ['id']

class WorkflowDefinitionSerializer(serializers.ModelSerializer):
    """مسلسل لتعريفات سير العمل"""
    created_by_name = serializers.SerializerMethodField()
    states_count = serializers.SerializerMethodField()
    states = WorkflowStateSerializer(many=True, read_only=True)
    
    class Meta:
        model = WorkflowDefinition
        fields = [
            'id', 'name', 'description', 'is_active', 
            'created_by', 'created_by_name', 'states_count', 'states'
        ]
        read_only_fields = ['id', 'created_by_name', 'states_count']
    
    def get_created_by_name(self, obj):
        return f"{obj.created_by.first_name} {obj.created_by.last_name}".strip() or obj.created_by.username
    
    def get_states_count(self, obj):
        return obj.states.count()

class WorkflowAssignmentSerializer(serializers.Serializer):
    """مسلسل لإسناد سير عمل إلى مستند"""
    document_id = serializers.IntegerField()
    initial_state_id = serializers.IntegerField(required=False)
    
    def validate_document_id(self, value):
        try:
            from documents.models import Document
            Document.objects.get(id=value)
        except ImportError:
            raise serializers.ValidationError("خطأ في النظام")
        except Document.DoesNotExist:
            raise serializers.ValidationError("المستند غير موجود")
        return value
    
    def validate_initial_state_id(self, value):
        if value:
            try:
                WorkflowState.objects.get(id=value)
            except WorkflowState.DoesNotExist:
                raise serializers.ValidationError("حالة سير العمل غير موجودة")
        return value