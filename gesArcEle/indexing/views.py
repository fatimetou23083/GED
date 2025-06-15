
# 2. indexing/views.py - النسخة المُصححة
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import IndexQueue, IndexingJob, IndexingStats
from .serializers import IndexQueueSerializer, IndexingJobSerializer, IndexingStatsSerializer

class IndexQueueViewSet(viewsets.ModelViewSet):
    queryset = IndexQueue.objects.all()  # إضافة queryset
    serializer_class = IndexQueueSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['GET'])
    def pending(self, request):
        pending_items = IndexQueue.objects.filter(status='PENDING')
        serializer = self.get_serializer(pending_items, many=True)
        return Response(serializer.data)

class IndexingJobViewSet(viewsets.ModelViewSet):
    queryset = IndexingJob.objects.all()  # إضافة queryset
    serializer_class = IndexingJobSerializer
    permission_classes = [permissions.IsAuthenticated]

class IndexingStatsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IndexingStats.objects.all()  # إضافة queryset
    serializer_class = IndexingStatsSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['POST'])
def reindex_all_documents(request):
    return Response({'message': 'تم بدء إعادة الفهرسة'})

@api_view(['POST']) 
def process_indexing_queue(request):
    return Response({'message': 'تم بدء معالجة قائمة الانتظار'})

# ------------------------------------------------------------------
