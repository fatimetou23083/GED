from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Permission
from .serializers import PermissionSerializer
from documents.models import Document  # Import supplémentaire
class PermissionViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les permissions des documents
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def by_document(self, request):
        """Permissions pour un document spécifique"""
        document_id = request.query_params.get('document_id')
        if not document_id:
            return Response({"error": "Le paramètre document_id est requis"}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        perms = Permission.objects.filter(document_id=document_id)
        serializer = self.get_serializer(perms, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_permissions(self, request):
        """Permissions de l'utilisateur connecté"""
        perms = Permission.objects.filter(user_id=request.user)
        serializer = self.get_serializer(perms, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def check_permission(self, request):
        """Vérifie si un utilisateur a une permission spécifique sur un document"""
        document_id = request.query_params.get('document_id')
        permission_type = request.query_params.get('permission_type')
        user_id = request.query_params.get('user_id', request.user.id)
        
        if not document_id or not permission_type:
            return Response({"error": "Les paramètres document_id et permission_type sont requis"}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        has_permission = Permission.objects.filter(
            document_id=document_id,
            user_id=user_id,
            permission_type=permission_type
        ).exists()
        
        return Response({"has_permission": has_permission})
    
    @action(detail=False, methods=['post'])
    def grant_permission(self, request):
        """Accorde une permission à un utilisateur sur un document"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Vérifie si l'utilisateur actuel est autorisé à accorder cette permission
            document_id = serializer.validated_data['document_id']
            
            # Vérifie si l'utilisateur est le créateur ou a des droits admin
            from documents.models import Document
            document = get_object_or_404(Document, id=document_id)
            
            if document.creator_id != request.user:
                admin_rights = Permission.objects.filter(
                    document_id=document_id,
                    user_id=request.user,
                    permission_type='ADMIN'
                ).exists()
                
                if not admin_rights:
                    return Response({"error": "Vous n'avez pas les droits pour accorder cette permission"}, 
                                   status=status.HTTP_403_FORBIDDEN)
            
            # Vérifie si la permission existe déjà
            document_id = serializer.validated_data['document_id']
            user_id = serializer.validated_data['user_id']
            permission_type = serializer.validated_data['permission_type']
            
            exists = Permission.objects.filter(
                document_id=document_id,
                user_id=user_id,
                permission_type=permission_type
            ).exists()
            
            if exists:
                return Response({"message": "Cette permission existe déjà"}, 
                               status=status.HTTP_200_OK)
            
            serializer.save(granted_at=timezone.now())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['delete'])
    def revoke_permission(self, request):
        """Révoque une permission"""
        document_id = request.query_params.get('document_id')
        user_id = request.query_params.get('user_id')
        permission_type = request.query_params.get('permission_type')
        
        if not all([document_id, user_id, permission_type]):
            return Response({"error": "Tous les paramètres sont requis"}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Vérifie si l'utilisateur actuel est autorisé à révoquer cette permission
        document = get_object_or_404(Document, id=document_id)
        
        if document.creator_id != request.user:
            admin_rights = Permission.objects.filter(
                document_id=document_id,
                user_id=request.user,
                permission_type='ADMIN'
            ).exists()
            
            if not admin_rights:
                return Response({"error": "Vous n'avez pas les droits pour révoquer cette permission"}, 
                               status=status.HTTP_403_FORBIDDEN)
        
        try:
            permission = Permission.objects.get(
                document_id=document_id,
                user_id=user_id,
                permission_type=permission_type
            )
            permission.delete()
            return Response({"message": "Permission révoquée avec succès"}, 
                           status=status.HTTP_200_OK)
        except Permission.DoesNotExist:
            return Response({"error": "Cette permission n'existe pas"}, 
                           status=status.HTTP_404_NOT_FOUND)