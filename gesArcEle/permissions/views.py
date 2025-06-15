# permissions/views.py - النسخة المصححة الكاملة
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Permission
from .serializers import PermissionSerializer

class DocumentPermissionViewSet(viewsets.ModelViewSet):
    """
    API endpoint لإدارة صلاحيات المستندات
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """تصفية الصلاحيات حسب المعايير"""
        queryset = Permission.objects.all()
        
        # تصفية حسب المستند
        document_id = self.request.query_params.get('document_id')
        if document_id:
            queryset = queryset.filter(document_id=document_id)
        
        # تصفية حسب المستخدم
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        # تصفية حسب نوع الصلاحية
        permission_type = self.request.query_params.get('permission_type')
        if permission_type:
            queryset = queryset.filter(permission_type=permission_type)
        
        return queryset
    
    @action(detail=False, methods=['GET'])
    def check(self, request):
        """التحقق من صلاحية معينة"""
        document_id = request.query_params.get('document_id')
        permission_type = request.query_params.get('permission_type')
        user_id = request.query_params.get('user_id', request.user.id)
        
        if not document_id or not permission_type:
            return Response(
                {'error': 'document_id و permission_type مطلوبان'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        has_permission = Permission.objects.filter(
            document_id=document_id,
            user_id=user_id,
            permission_type=permission_type
        ).exists()
        
        return Response({
            'has_permission': has_permission,
            'document_id': document_id,
            'user_id': user_id,
            'permission_type': permission_type
        })
    
    @action(detail=False, methods=['POST'])
    def bulk_assign(self, request):
        """إسناد صلاحيات متعددة"""
        document_id = request.data.get('document_id')
        permissions_data = request.data.get('permissions', [])
        
        if not document_id or not permissions_data:
            return Response(
                {'error': 'document_id و permissions مطلوبان'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # استيراد محلي لتجنب المشاكل الدائرية
            from documents.models import Document
            from users.models import User
            
            document = Document.objects.get(id=document_id)
        except ImportError:
            return Response(
                {'error': 'خطأ في النظام'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Document.DoesNotExist:
            return Response(
                {'error': 'المستند غير موجود'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        created_permissions = []
        
        for perm_data in permissions_data:
            user_id = perm_data.get('user_id')
            permission_type = perm_data.get('permission_type')
            
            if user_id and permission_type:
                try:
                    user = User.objects.get(id=user_id)
                    permission, created = Permission.objects.get_or_create(
                        document=document,
                        user=user,
                        permission_type=permission_type
                    )
                    
                    if created:
                        created_permissions.append(permission)
                        
                except User.DoesNotExist:
                    continue
        
        return Response({
            'message': f'تم إنشاء {len(created_permissions)} صلاحية',
            'created_count': len(created_permissions)
        })
    
    @action(detail=False, methods=['DELETE'])
    def bulk_remove(self, request):
        """حذف صلاحيات متعددة"""
        document_id = request.data.get('document_id')
        user_ids = request.data.get('user_ids', [])
        permission_type = request.data.get('permission_type')
        
        if not document_id:
            return Response(
                {'error': 'document_id مطلوب'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        filters = {'document_id': document_id}
        
        if user_ids:
            filters['user_id__in'] = user_ids
        
        if permission_type:
            filters['permission_type'] = permission_type
        
        deleted_count = Permission.objects.filter(**filters).delete()[0]
        
        return Response({
            'message': f'تم حذف {deleted_count} صلاحية',
            'deleted_count': deleted_count
        })
    
    @action(detail=False, methods=['GET'])
    def my_permissions(self, request):
        """صلاحيات المستخدم الحالي"""
        permissions = Permission.objects.filter(user=request.user)
        
        document_id = request.query_params.get('document_id')
        if document_id:
            permissions = permissions.filter(document_id=document_id)
        
        serializer = self.get_serializer(permissions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def by_document(self, request):
        """جميع صلاحيات مستند معين"""
        document_id = request.query_params.get('document_id')
        
        if not document_id:
            return Response(
                {'error': 'document_id مطلوب'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        permissions = Permission.objects.filter(document_id=document_id)
        serializer = self.get_serializer(permissions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def stats(self, request):
        """إحصائيات الصلاحيات"""
        from django.db.models import Count
        
        stats = {
            'total_permissions': Permission.objects.count(),
            'permissions_by_type': dict(
                Permission.objects.values('permission_type').annotate(
                    count=Count('id')
                ).values_list('permission_type', 'count')
            ),
            'users_with_permissions': Permission.objects.values('user').distinct().count(),
            'documents_with_permissions': Permission.objects.values('document').distinct().count(),
        }
        
        return Response(stats)