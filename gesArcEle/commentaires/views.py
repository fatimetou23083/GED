from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Comment
from .serializers import CommentSerializer, CommentCreateSerializer, CommentTreeSerializer

class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les commentaires
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return CommentCreateSerializer
        elif self.action == 'retrieve' or self.action == 'list':
            return CommentSerializer
        return super().get_serializer_class()
    
    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user)
    
    @action(detail=False, methods=['get'])
    def by_document(self, request):
        """Récupérer tous les commentaires d'un document"""
        document_id = request.query_params.get('document_id')
        if not document_id:
            return Response({"error": "Le paramètre document_id est requis"}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Récupère les commentaires de premier niveau (sans parent)
        comments = Comment.objects.filter(document_id=document_id, parent_id=None)
        serializer = CommentTreeSerializer(comments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def replies(self, request, pk=None):
        """Récupérer les réponses à un commentaire"""
        comment = self.get_object()
        replies = Comment.objects.filter(parent_id=comment.id)
        serializer = self.get_serializer(replies, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_comments(self, request):
        """Récupérer les commentaires de l'utilisateur connecté"""
        comments = Comment.objects.filter(author_id=request.user)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)