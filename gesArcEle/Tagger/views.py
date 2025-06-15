# Tagger/views.py - النسخة النهائية المُصححة
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import Tag, DocumentTag
from .serializers import TagSerializer, DocumentTagSerializer

class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint لإدارة العلامات
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['POST'])
    def assign_to_document(self, request, pk=None):
        """إسناد علامة إلى مستند"""
        tag = self.get_object()
        document_id = request.data.get('document_id')
        
        if not document_id:
            return Response(
                {'error': 'document_id مطلوب'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from documents.models import Document
            document = Document.objects.get(id=document_id)
            
            document_tag, created = DocumentTag.objects.get_or_create(
                document=document,
                tag=tag
            )
            
            return Response({
                'message': 'تم إسناد العلامة' if created else 'العلامة مسندة مسبقاً',
                'created': created
            })
            
        except Document.DoesNotExist:
            return Response(
                {'error': 'المستند غير موجود'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['DELETE'])
    def remove_from_document(self, request, pk=None):
        """إزالة علامة من مستند"""
        tag = self.get_object()
        document_id = request.data.get('document_id')
        
        if not document_id:
            return Response(
                {'error': 'document_id مطلوب'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        deleted_count = DocumentTag.objects.filter(
            document_id=document_id,
            tag=tag
        ).delete()[0]
        
        return Response({
            'message': 'تم إزالة العلامة' if deleted_count > 0 else 'العلامة غير موجودة',
            'deleted': deleted_count > 0
        })
    
    @action(detail=False, methods=['GET'])
    def popular(self, request):
        """العلامات الأكثر استخداماً"""
        tags = Tag.objects.annotate(
            usage_count=Count('tag_documents')
        ).order_by('-usage_count')[:20]
        
        serializer = self.get_serializer(tags, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['GET'])
    def documents(self, request, pk=None):
        """الحصول على جميع المستندات مع هذه العلامة"""
        tag = self.get_object()
        
        try:
            from documents.models import Document
            from documents.serializers import DocumentSerializer
            
            documents = Document.objects.filter(
                document_tags__tag=tag,
                is_deleted=False
            )
            
            serializer = DocumentSerializer(documents, many=True)
            return Response(serializer.data)
        except ImportError:
            return Response(
                {'error': 'خطأ في النظام'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DocumentTagViewSet(viewsets.ModelViewSet):
    """
    API endpoint لإدارة ربط المستندات بالعلامات
    """
    queryset = DocumentTag.objects.all()
    serializer_class = DocumentTagSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """تصفية حسب المستند أو العلامة إذا تم تحديدها"""
        queryset = DocumentTag.objects.all()
        
        document_id = self.request.query_params.get('document_id')
        if document_id:
            queryset = queryset.filter(document_id=document_id)
        
        tag_id = self.request.query_params.get('tag_id')
        if tag_id:
            queryset = queryset.filter(tag_id=tag_id)
        
        return queryset
    
    @action(detail=False, methods=['POST'])
    def bulk_assign(self, request):
        """إسناد عدة علامات لمستند"""
        document_id = request.data.get('document_id')
        tag_ids = request.data.get('tag_ids', [])
        
        if not document_id or not tag_ids:
            return Response(
                {'error': 'document_id و tag_ids مطلوبان'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from documents.models import Document
            document = Document.objects.get(id=document_id)
            
            created_count = 0
            for tag_id in tag_ids:
                try:
                    tag = Tag.objects.get(id=tag_id)
                    _, created = DocumentTag.objects.get_or_create(
                        document=document,
                        tag=tag
                    )
                    if created:
                        created_count += 1
                except Tag.DoesNotExist:
                    continue
            
            return Response({
                'message': f'تم إسناد {created_count} علامة',
                'created_count': created_count
            })
            
        except Document.DoesNotExist:
            return Response(
                {'error': 'المستند غير موجود'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['DELETE'])
    def bulk_remove(self, request):
        """إزالة عدة علامات من مستند"""
        document_id = request.data.get('document_id')
        tag_ids = request.data.get('tag_ids', [])
        
        if not document_id:
            return Response(
                {'error': 'document_id مطلوب'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        filters = {'document_id': document_id}
        if tag_ids:
            filters['tag_id__in'] = tag_ids
        
        deleted_count = DocumentTag.objects.filter(**filters).delete()[0]
        
        return Response({
            'message': f'تم إزالة {deleted_count} علامة',
            'deleted_count': deleted_count
        })