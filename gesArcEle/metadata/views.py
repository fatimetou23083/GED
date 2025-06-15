
# 3. metadata/views.py - النسخة المُصححة
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import MetadataType
from .serializers import MetadataTypeSerializer

class MetadataTypeViewSet(viewsets.ModelViewSet):
    queryset = MetadataType.objects.all()  # إضافة queryset
    serializer_class = MetadataTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['POST'])
    def assign_to_document(self, request, pk=None):
        metadata_type = self.get_object()
        document_id = request.data.get('document_id')
        value = request.data.get('value')
        
        if not document_id or not value:
            return Response(
                {'error': 'document_id و value مطلوبان'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from documents.models import Document, Metadata
            document = Document.objects.get(id=document_id)
            
            metadata, created = Metadata.objects.update_or_create(
                document=document,
                key=metadata_type.name,
                defaults={
                    'value_text': str(value),
                    'value_type': metadata_type.data_type
                }
            )
            
            return Response({
                'message': 'تم إضافة البيانات الوصفية' if created else 'تم تحديث البيانات الوصفية',
                'metadata_id': metadata.id
            })
            
        except Document.DoesNotExist:
            return Response(
                {'error': 'المستند غير موجود'}, 
                status=status.HTTP_404_NOT_FOUND
            )

# ------------------------------------------------------------------
