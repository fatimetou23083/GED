# cabinets/views.py - VERSION CORRIGÉE
from django.shortcuts import get_object_or_404
from django.db import models
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cabinet
from .serializers import CabinetSerializer, CabinetTreeSerializer

class CabinetViewSet(viewsets.ModelViewSet):
    """
    API endpoint لإدارة الخزائن/الملفات
    """
    queryset = Cabinet.objects.all()
    serializer_class = CabinetSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """تصفية الخzائن حسب المعايير والصلاحيات"""
        queryset = Cabinet.objects.all()
        
        # تصفية حسب المالك إذا لم يكن المستخدم مديراً
        if not self.request.user.is_staff:
            queryset = queryset.filter(
                models.Q(is_private=False) | 
                models.Q(owner=self.request.user)
            )
        
        # تصفية حسب الأب
        parent_id = self.request.query_params.get('parent_id')
        if parent_id:
            if parent_id == 'null':
                queryset = queryset.filter(parent__isnull=True)
            else:
                queryset = queryset.filter(parent_id=parent_id)
        
        return queryset
    
    def get_serializer_class(self):
        """تحديد المسلسل المستخدم"""
        if self.action == 'tree':
            return CabinetTreeSerializer
        return CabinetSerializer
    
    def perform_create(self, serializer):
        """إنشاء خزانة مع المستخدم الحالي كمالك"""
        serializer.save(owner=self.request.user)
    
    @action(detail=False, methods=['GET'])
    def tree(self, request):
        """الحصول على هيكل شجرة الخزائن الكامل"""
        root_cabinets = self.get_queryset().filter(parent__isnull=True)
        serializer = CabinetTreeSerializer(root_cabinets, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def my_cabinets(self, request):
        """الحصول على خزائن المستخدم الحالي"""
        cabinets = Cabinet.objects.filter(owner=request.user)
        serializer = self.get_serializer(cabinets, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['GET'])
    def documents(self, request, pk=None):
        """الحصول على مستندات خزانة"""
        cabinet = self.get_object()
        
        # التحقق من الصلاحيات
        if cabinet.is_private and cabinet.owner != request.user and not request.user.is_staff:
            return Response(
                {'error': 'الصلاحية مرفوضة'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            from documents.models import Document
            from documents.serializers import DocumentSerializer
            
            documents = Document.objects.filter(
                cabinet=cabinet,
                is_deleted=False
            ).order_by('-created_at')
            
            # الصفحات
            page_size = int(request.query_params.get('page_size', 25))
            page = int(request.query_params.get('page', 1))
            start = (page - 1) * page_size
            end = start + page_size
            
            paginated_documents = documents[start:end]
            serializer = DocumentSerializer(paginated_documents, many=True)
            
            return Response({
                'documents': serializer.data,
                'total': documents.count(),
                'page': page,
                'page_size': page_size,
                'has_next': end < documents.count()
            })
        except ImportError:
            return Response(
                {'error': 'خطأ في النظام'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['GET'])
    def subcabinets(self, request, pk=None):
        """الحصول على الخزائن الفرعية"""
        cabinet = self.get_object()
        subcabinets = Cabinet.objects.filter(parent=cabinet)
        
        # تصفية حسب الصلاحيات
        if not request.user.is_staff:
            subcabinets = subcabinets.filter(
                models.Q(is_private=False) | 
                models.Q(owner=request.user)
            )
        
        serializer = self.get_serializer(subcabinets, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['POST'])
    def move(self, request, pk=None):
        """نقل خزانة إلى أب جديد"""
        cabinet = self.get_object()
        new_parent_id = request.data.get('new_parent_id')
        
        # التحقق من الصلاحيات
        if cabinet.owner != request.user and not request.user.is_staff:
            return Response(
                {'error': 'الصلاحية مرفوضة'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # إدارة النقل إلى الجذر
        if new_parent_id in [None, 'null', '']:
            cabinet.parent = None
        else:
            try:
                new_parent = Cabinet.objects.get(id=new_parent_id)
                
                # التحقق من عدم إنشاء حلقة مفرغة
                current = new_parent
                while current:
                    if current.id == cabinet.id:
                        return Response(
                            {'error': 'لا يمكن إنشاء حلقة في التسلسل الهرمي'}, 
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    current = current.parent
                
                cabinet.parent = new_parent
                
            except Cabinet.DoesNotExist:
                return Response(
                    {'error': 'الخزانة الأب غير موجودة'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        cabinet.save()
        serializer = self.get_serializer(cabinet)
        return Response(serializer.data)
    
    @action(detail=True, methods=['POST'])
    def toggle_privacy(self, request, pk=None):
        """تبديل خصوصية خزانة (خاص/عام)"""
        cabinet = self.get_object()
        
        # فقط المالك أو المدير يمكن تعديل الخصوصية
        if cabinet.owner != request.user and not request.user.is_staff:
            return Response(
                {'error': 'الصلاحية مرفوضة'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        cabinet.is_private = not cabinet.is_private
        cabinet.save()
        
        return Response({
            'is_private': cabinet.is_private,
            'message': 'تم جعل الخزانة خاصة' if cabinet.is_private else 'تم جعل الخزانة عامة'
        })
    
    @action(detail=False, methods=['GET'])
    def search(self, request):
        """البحث في الخزائن"""
        query = request.query_params.get('q', '')
        
        if not query:
            return Response(
                {'error': 'معامل البحث مطلوب'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cabinets = self.get_queryset().filter(
            models.Q(name__icontains=query) |
            models.Q(description__icontains=query)
        )
        
        serializer = self.get_serializer(cabinets, many=True)
        return Response(serializer.data)