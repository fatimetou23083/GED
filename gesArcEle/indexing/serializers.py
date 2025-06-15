# ==============================================================================
# إنشاء جميع serializers المطلوبة
# ==============================================================================

# indexing/serializers.py
from rest_framework import serializers
from .models import IndexQueue, IndexingJob, IndexingStats

class IndexQueueSerializer(serializers.ModelSerializer):
    document_title = serializers.SerializerMethodField()
    
    class Meta:
        model = IndexQueue
        fields = ['id', 'document_id', 'document_title', 'status', 'created_at', 
                 'processed_at', 'error_message', 'retry_count']
        read_only_fields = ['id', 'created_at', 'processed_at', 'document_title']
    
    def get_document_title(self, obj):
        return obj.document.title if obj.document else ""

class IndexingJobSerializer(serializers.ModelSerializer):
    document_title = serializers.SerializerMethodField()
    
    class Meta:
        model = IndexingJob
        fields = ['id', 'document_id', 'document_title', 'job_type', 'status', 
                 'started_at', 'completed_at', 'result_data', 'error_message']
        read_only_fields = ['id', 'document_title']
    
    def get_document_title(self, obj):
        return obj.document.title if obj.document else ""

class IndexingStatsSerializer(serializers.ModelSerializer):
    success_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = IndexingStats
        fields = ['id', 'date', 'total_documents', 'indexed_documents', 
                 'failed_documents', 'processing_time_avg', 'success_rate']
        read_only_fields = ['id', 'success_rate']
    
    def get_success_rate(self, obj):
        if obj.total_documents > 0:
            return (obj.indexed_documents / obj.total_documents) * 100
        return 0

