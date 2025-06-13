import os
from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.parsers import MultiPartParser, FormParser
from Catalog.models import Category  
from documents.models import Document, DocumentVersion
from .serializers import CategorySerializer, DocumentSerializer, DocumentDetailSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    Point d'entrée API pour visualiser et éditer les catégories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        """Sauvegarde la catégorie"""
        serializer.save()
    
    @action(detail=True, methods=['get'])
    def subcategories(self, request, pk=None):
        """Récupère les sous-catégories d'une catégorie"""
        category = self.get_object()
        subcats = Category.objects.filter(parent_id=category.id)
        serializer = self.get_serializer(subcats, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def documents(self, request, pk=None):
        """Récupère les documents dans une catégorie"""
        category = self.get_object()
        documents = Document.objects.filter(category_id=category.id)
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

class DocumentViewSet(viewsets.ModelViewSet):
    """
    Point d'entrée API pour gérer les documents d'archive.
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DocumentDetailSerializer
        return DocumentSerializer
    
    def perform_create(self, serializer):
        """Associe l'utilisateur connecté comme créateur du document"""
        serializer.save(creator=self.request.user)
    
    def perform_update(self, serializer):
        """Met à jour le document"""
        serializer.save()
    
    def perform_destroy(self, instance):
        """Supprime le document et ses fichiers associés"""
        # Supprimer les fichiers
        for version in instance.versions.all():
            file_path = os.path.join(settings.MEDIA_ROOT, version.file_path)
            try:
                os.remove(file_path)
            except OSError:
                pass
        
        # Supprimer le répertoire du document s'il est vide
        try:
            doc_dir = os.path.join(settings.MEDIA_ROOT, 'documents', str(instance.id))
            os.rmdir(doc_dir)
        except OSError:
            pass
        
        # Supprimer l'instance
        instance.delete()
    
    @action(detail=True, methods=['get'])
    def download_latest(self, request, pk=None):
        """Télécharge la dernière version du document"""
        document = self.get_object()
        try:
            latest_version = document.versions.latest('version_number')
            file_path = os.path.join(settings.MEDIA_ROOT, latest_version.file_path)
            if os.path.exists(file_path):
                response = FileResponse(open(file_path, 'rb'))
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                return response
        except DocumentVersion.DoesNotExist:
            pass
        
        return Response(
            {"error": "Fichier non trouvé"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """Filtre les documents par leur statut"""
        status_param = request.query_params.get('status', '')
        if not status_param:
            return Response({"error": "Le paramètre 'status' est requis"}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        documents = Document.objects.filter(status=status_param)
        serializer = self.get_serializer(documents, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def metadata(self, request, pk=None):
        """Récupère les métadonnées d'un document"""
        document = self.get_object()
        
        # Import ici pour éviter les problèmes d'importation circulaire
        from documents.models import Metadata
        from documents.serializers import MetadataSerializer
        
        metadata = Metadata.objects.filter(document_id=document.id)
        serializer = MetadataSerializer(metadata, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def versions(self, request, pk=None):
        """Récupère les versions d'un document"""
        document = self.get_object()
        
        # Import ici pour éviter les problèmes d'importation circulaire
        from documents.models import DocumentVersion
        from documents.serializers import DocumentVersionSerializer
        
        versions = DocumentVersion.objects.filter(document_id=document.id)
        serializer = DocumentVersionSerializer(versions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def tags(self, request, pk=None):
        """Récupère les tags d'un document"""
        document = self.get_object()
        
        # Import ici pour éviter les problèmes d'importation circulaire
        from Tagger.models import Tag
        from Tagger.serializers import TagSerializer
        
        # Utilise la relation many-to-many via DocumentTag
        tags = Tag.objects.filter(documenttag__document_id=document.id)
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Récupère les commentaires d'un document"""
        document = self.get_object()
        
        # Import ici pour éviter les problèmes d'importation circulaire
        from commentaires.models import Comment
        from commentaires.serializers import CommentSerializer
        
        comments = Comment.objects.filter(document_id=document.id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def permissions(self, request, pk=None):
        """Récupère les permissions d'un document"""
        document = self.get_object()
        
        # Import ici pour éviter les problèmes d'importation circulaire
        from permissions.models import Permission
        from permissions.serializers import PermissionSerializer
        
        perms = Permission.objects.filter(document_id=document.id)
        serializer = PermissionSerializer(perms, many=True)
        return Response(serializer.data)
    
    
    def create(self, request, *args, **kwargs):
        """Créer un nouveau document avec upload de fichier"""
        try:
            print(f"📥 Données reçues: {request.data}")
            print(f"📁 Fichiers reçus: {request.FILES}")
            
            # Vérifier les données requises
            if not request.data.get('title'):
                return Response(
                    {"error": "Le titre est requis"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not request.data.get('category_id'):
                return Response(
                    {"error": "La catégorie est requise"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Vérifier que la catégorie existe
            try:
                category = Category.objects.get(id=request.data.get('category_id'))
            except Category.DoesNotExist:
                return Response(
                    {"error": "Catégorie non trouvée"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Créer le document
            document = Document.objects.create(
                title=request.data.get('title'),
                description=request.data.get('description', ''),
                category=category,
                status=request.data.get('status', 'DRAFT'),
                creator=request.user
            )
            
            print(f"✅ Document créé: {document.id}")
            
            # Gérer le fichier si présent
            if 'file' in request.FILES:
                file_obj = request.FILES['file']
                print(f"📎 Traitement fichier: {file_obj.name} ({file_obj.size} bytes)")
                
                # Vérifier la taille du fichier (50MB max)
                if file_obj.size > 50 * 1024 * 1024:
                    document.delete()
                    return Response(
                        {"error": "Fichier trop volumineux (max 50MB)"}, 
                        status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
                    )
                
                # Créer le répertoire pour ce document
                import os
                document_dir = os.path.join(settings.MEDIA_ROOT, 'documents', str(document.id))
                os.makedirs(document_dir, exist_ok=True)
                
                # Générer le nom du fichier
                file_ext = os.path.splitext(file_obj.name)[1]
                safe_filename = f"document_{document.id}_v1{file_ext}"
                file_path = os.path.join(document_dir, safe_filename)
                relative_path = os.path.join('documents', str(document.id), safe_filename)
                
                # Sauvegarder le fichier
                with open(file_path, 'wb+') as destination:
                    for chunk in file_obj.chunks():
                        destination.write(chunk)
                
                # Créer la version du document
                DocumentVersion.objects.create(
                    document=document,
                    version_number=1,
                    file_path=relative_path,
                    created_by=request.user
                )
                
                print(f"💾 Fichier sauvegardé: {relative_path}")
            
            # Retourner la réponse
            serializer = self.get_serializer(document)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(f"❌ Erreur lors de l'upload: {str(e)}")
            return Response(
                {"error": f"Erreur serveur: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SearchView(viewsets.ViewSet):
    """
    Point d'entrée API pour la recherche dans les archives
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def search_documents(self, request):
        """Recherche dans les documents"""
        query = request.query_params.get('q', '')
        if not query:
            return Response({"error": "Le paramètre de recherche 'q' est requis"}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Import ici pour éviter les problèmes d'importation circulaire
        from .models import SearchIndex
        
        # Recherche dans l'index
        results = SearchIndex.objects.filter(
            content_text__icontains=query
        ) | SearchIndex.objects.filter(
            metadata_text__icontains=query
        )
        
        # Récupère les documents associés
        document_ids = results.values_list('document_id', flat=True)
        documents = Document.objects.filter(id__in=document_ids)
        
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)