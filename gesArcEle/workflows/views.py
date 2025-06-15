# workflows/views.py - النسخة الصحيحة النهائية
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import WorkflowDefinition, WorkflowState
from .serializers import WorkflowDefinitionSerializer, WorkflowStateSerializer, WorkflowAssignmentSerializer

class WorkflowDefinitionViewSet(viewsets.ModelViewSet):
    """
    API endpoint لإدارة تعريفات سير العمل
    """
    queryset = WorkflowDefinition.objects.all()
    serializer_class = WorkflowDefinitionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """تصفية سير العمل النشط افتراضياً"""
        if self.request.query_params.get('include_inactive') == 'true':
            return WorkflowDefinition.objects.all()
        return WorkflowDefinition.objects.filter(is_active=True)
    
    def perform_create(self, serializer):
        """إنشاء سير عمل مع المستخدم الحالي كمنشئ"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['GET'])
    def get_states(self, request, pk=None):
        """الحصول على حالات سير عمل"""
        workflow = self.get_object()
        states = workflow.states.all().order_by('name')
        serializer = WorkflowStateSerializer(states, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['POST'])
    def assign_to_document(self, request, pk=None):
        """إسناد سير عمل إلى مستند"""
        workflow = self.get_object()
        serializer = WorkflowAssignmentSerializer(data=request.data)
        
        if serializer.is_valid():
            document_id = serializer.validated_data['document_id']
            initial_state_id = serializer.validated_data.get('initial_state_id')
            
            try:
                from documents.models import Document
                document = Document.objects.get(id=document_id)
                
                # تحديد الحالة الأولية
                if initial_state_id:
                    initial_state = WorkflowState.objects.get(
                        id=initial_state_id,
                        workflow=workflow
                    )
                else:
                    # أخذ أول حالة مُعلَّمة كأولية
                    initial_state = workflow.states.filter(is_initial=True).first()
                    if not initial_state:
                        # وإلا أخذ أول حالة
                        initial_state = workflow.states.first()
                
                if not initial_state:
                    return Response(
                        {'error': 'لا توجد حالات متاحة لسير العمل هذا'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # إسناد سير العمل والحالة
                document.workflow_state = initial_state
                document.save()
                
                return Response({
                    'message': 'تم إسناد سير العمل بنجاح',
                    'document_id': document.id,
                    'workflow_id': workflow.id,
                    'current_state_id': initial_state.id,
                    'current_state_name': initial_state.label
                })
                
            except Document.DoesNotExist:
                return Response(
                    {'error': 'المستند غير موجود'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            except WorkflowState.DoesNotExist:
                return Response(
                    {'error': 'الحالة الأولية غير موجودة'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['POST'])
    def toggle_active(self, request, pk=None):
        """تفعيل/إلغاء تفعيل سير عمل"""
        workflow = self.get_object()
        
        # فقط المنشئ أو المدير يمكنه التعديل
        if workflow.created_by != request.user and not request.user.is_staff:
            return Response(
                {'error': 'الصلاحية مرفوضة'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        workflow.is_active = not workflow.is_active
        workflow.save()
        
        return Response({
            'is_active': workflow.is_active,
            'message': 'تم تفعيل سير العمل' if workflow.is_active else 'تم إلغاء تفعيل سير العمل'
        })
    
    @action(detail=False, methods=['GET'])
    def my_workflows(self, request):
        """الحصول على سير العمل المُنشَأ بواسطة المستخدم الحالي"""
        workflows = WorkflowDefinition.objects.filter(created_by=request.user)
        serializer = self.get_serializer(workflows, many=True)
        return Response(serializer.data)

class WorkflowStateViewSet(viewsets.ModelViewSet):
    """
    API endpoint لإدارة حالات سير العمل
    """
    queryset = WorkflowState.objects.all()
    serializer_class = WorkflowStateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """تصفية الحالات حسب سير العمل إذا تم تحديده"""
        queryset = WorkflowState.objects.all()
        
        workflow_id = self.request.query_params.get('workflow_id')
        if workflow_id:
            queryset = queryset.filter(workflow_id=workflow_id)
        
        return queryset
    
    @action(detail=False, methods=['GET'])
    def initial_states(self, request):
        """الحصول على جميع الحالات الأولية"""
        states = WorkflowState.objects.filter(is_initial=True)
        serializer = self.get_serializer(states, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def final_states(self, request):
        """الحصول على جميع الحالات النهائية"""
        states = WorkflowState.objects.filter(is_final=True)
        serializer = self.get_serializer(states, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['GET'])
    def documents(self, request, pk=None):
        """الحصول على المستندات في هذه الحالة"""
        state = self.get_object()
        
        try:
            from documents.models import Document
            from documents.serializers import DocumentSerializer
            
            documents = Document.objects.filter(
                workflow_state=state,
                is_deleted=False
            )
            
            serializer = DocumentSerializer(documents, many=True)
            return Response(serializer.data)
        except ImportError:
            return Response(
                {'error': 'خطأ في النظام'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )