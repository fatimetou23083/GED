# messaging/views.py - النسخة المصححة مع queryset
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Message, Notification, MessageTemplate
from .serializers import MessageSerializer, NotificationSerializer, MessageTemplateSerializer

class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint لإدارة الرسائل
    """
    # إضافة queryset أساسي (سيتم تصفيته في get_queryset)
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """تصفية الرسائل للمستخدم الحالي"""
        return Message.objects.filter(recipient=self.request.user)
    
    def perform_create(self, serializer):
        """إنشاء رسالة مع المرسل الحالي"""
        serializer.save(sender=self.request.user)
    
    @action(detail=False, methods=['GET'])
    def unread(self, request):
        """الحصول على الرسائل غير المقروءة"""
        unread_messages = Message.objects.filter(
            recipient=request.user,
            is_read=False
        )
        serializer = self.get_serializer(unread_messages, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def unread_count(self, request):
        """عدد الرسائل غير المقروءة"""
        count = Message.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()
        return Response({'unread_count': count})
    
    @action(detail=True, methods=['POST'])
    def mark_read(self, request, pk=None):
        """تحديد رسالة كمقروءة"""
        message = self.get_object()
        message.is_read = True
        message.read_at = timezone.now()
        message.save()
        
        return Response({'message': 'تم تحديد الرسالة كمقروءة'})
    
    @action(detail=False, methods=['POST'])
    def mark_all_read(self, request):
        """تحديد جميع الرسائل كمقروءة"""
        updated_count = Message.objects.filter(
            recipient=request.user,
            is_read=False
        ).update(
            is_read=True,
            read_at=timezone.now()
        )
        
        return Response({
            'message': f'تم تحديد {updated_count} رسالة كمقروءة',
            'updated_count': updated_count
        })
    
    @action(detail=False, methods=['GET'])
    def by_type(self, request):
        """تصفية الرسائل حسب النوع"""
        message_type = request.query_params.get('type')
        
        if not message_type:
            return Response(
                {'error': 'معامل النوع مطلوب'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        messages = Message.objects.filter(
            recipient=request.user,
            message_type=message_type
        )
        
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

class NotificationViewSet(viewsets.ModelViewSet):
    """
    API endpoint لإدارة الإشعارات
    """
    # إضافة queryset أساسي
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """تصفية الإشعارات للمستخدم الحالي"""
        return Notification.objects.filter(recipients=self.request.user)
    
    @action(detail=False, methods=['GET'])
    def my_notifications(self, request):
        """الحصول على إشعارات المستخدم مع حالة القراءة"""
        notifications = Notification.objects.filter(
            recipients=request.user
        ).prefetch_related('notificationrecipient_set')
        
        notification_data = []
        for notification in notifications:
            try:
                from .models import NotificationRecipient
                recipient_data = notification.notificationrecipient_set.filter(
                    user=request.user
                ).first()
                
                data = self.get_serializer(notification).data
                data['is_read'] = recipient_data.is_read if recipient_data else False
                data['read_at'] = recipient_data.read_at if recipient_data else None
                
                notification_data.append(data)
            except:
                # في حالة عدم وجود NotificationRecipient
                data = self.get_serializer(notification).data
                data['is_read'] = False
                data['read_at'] = None
                notification_data.append(data)
        
        return Response(notification_data)
    
    @action(detail=True, methods=['POST'])
    def mark_read(self, request, pk=None):
        """تحديد إشعار كمقروء"""
        notification = self.get_object()
        
        try:
            from .models import NotificationRecipient
            recipient, created = NotificationRecipient.objects.get_or_create(
                notification=notification,
                user=request.user,
                defaults={'is_read': True, 'read_at': timezone.now()}
            )
            
            if not created and not recipient.is_read:
                recipient.is_read = True
                recipient.read_at = timezone.now()
                recipient.save()
        except:
            pass  # تجاهل الأخطاء إذا لم يكن النموذج موجوداً
        
        return Response({'message': 'تم تحديد الإشعار كمقروء'})
    
    @action(detail=False, methods=['POST'])
    def broadcast(self, request):
        """بث إشعار لجميع المستخدمين (المديرون فقط)"""
        if not request.user.is_staff:
            return Response(
                {'error': 'الصلاحية مرفوضة'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        title = request.data.get('title')
        message = request.data.get('message')
        notification_type = request.data.get('notification_type', 'SYSTEM_MAINTENANCE')
        
        if not title or not message:
            return Response(
                {'error': 'العنوان والرسالة مطلوبان'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # إنشاء الإشعار
        notification = Notification.objects.create(
            notification_type=notification_type,
            title=title,
            message=message,
            is_system=True
        )
        
        # إضافة جميع المستخدمين النشطين
        from users.models import User
        active_users = User.objects.filter(is_active=True)
        notification.recipients.set(active_users)
        
        return Response({
            'message': f'تم بث الإشعار إلى {active_users.count()} مستخدم',
            'notification_id': notification.id
        })

class MessageTemplateViewSet(viewsets.ModelViewSet):
    """
    API endpoint لإدارة قوالب الرسائل
    """
    queryset = MessageTemplate.objects.all()
    serializer_class = MessageTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['POST'])
    def send_message(self, request, pk=None):
        """إرسال رسالة بناءً على قالب"""
        template = self.get_object()
        recipient_id = request.data.get('recipient_id')
        variables = request.data.get('variables', {})
        
        if not recipient_id:
            return Response(
                {'error': 'recipient_id مطلوب'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from users.models import User
            recipient = User.objects.get(id=recipient_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'المستلم غير موجود'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # استبدال المتغيرات في القالب
        try:
            title = template.subject_template.format(**variables)
            content = template.body_template.format(**variables)
        except KeyError as e:
            return Response(
                {'error': f'متغير مفقود: {e}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # إنشاء الرسالة
        message = Message.objects.create(
            title=title,
            content=content,
            message_type=template.message_type,
            recipient=recipient,
            sender=request.user
        )
        
        return Response({
            'message': 'تم إرسال الرسالة بنجاح',
            'message_id': message.id
        })