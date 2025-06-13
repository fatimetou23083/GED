from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Tag, DocumentTag
from .serializers import TagSerializer, DocumentTagSerializer

class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les tags
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def by_document(self, request):
        """Tags associés à un document"""
        document_id = request.query_params.get('document_id')
        if not document_id:
            return Response({"error": "Le paramètre document_id est requis"}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        tags = Tag.objects.filter(documenttag__document_id=document_id)
        serializer = self.get_serializer(tags, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def documents(self, request, pk=None):
        """Documents associés à un tag"""
        tag = self.get_object()
        
        # Import ici pour éviter les problèmes d'importation circulaire
        from documents.models import Document
        from documents.serializers import DocumentSerializer
        
        documents = Document.objects.filter(documenttag__tag_id=tag.id)
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

class DocumentTagViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les associations document-tag
    """
    queryset = DocumentTag.objects.all()
    serializer_class = DocumentTagSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def tag_document(self, request):
        """Associer un tag à un document"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Vérifie si l'association existe déjà
            document_id = serializer.validated_data['document_id']
            tag_id = serializer.validated_data['tag_id']
            
            exists = DocumentTag.objects.filter(
                document_id=document_id,
                tag_id=tag_id
            ).exists()
            
            if exists:
                return Response({"message": "Cette association existe déjà"}, 
                               status=status.HTTP_200_OK)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['delete'])
    def untag_document(self, request):
        """Supprimer l'association entre un tag et un document"""
        document_id = request.query_params.get('document_id')
        tag_id = request.query_params.get('tag_id')
        
        if not document_id or not tag_id:
            return Response({"error": "Les paramètres document_id et tag_id sont requis"}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        try:
            tag_relation = DocumentTag.objects.get(document_id=document_id, tag_id=tag_id)
            tag_relation.delete()
            return Response({"message": "Tag retiré avec succès"}, status=status.HTTP_200_OK)
        except DocumentTag.DoesNotExist:
            return Response({"error": "Cette association n'existe pas"}, 
                           status=status.HTTP_404_NOT_FOUND)