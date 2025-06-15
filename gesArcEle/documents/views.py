# documents/views.py - CORRECTION DES NOMS DE MÉTHODES
import os
import hashlib
from datetime import datetime, timedelta
from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q, Count, Sum
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage

# Imports des modèles locaux
from .models import Document, DocumentVersion, DocumentAccess, Metadata, SearchIndex, DocumentType

# Imports des serializers
from .serializers import DocumentSerializer, DocumentDetailSerializer, DocumentVersionSerializer

# Imports des autres modèles (avec protection contre les erreurs)
try:
    from Catalog.models import Category
except ImportError:
    from Catalog.models import Category

try:
    from users.models import User
except ImportError:
    from django.contrib.auth import get_user_model
    User = get_user_model()

class DocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet Document avec TOUTES les fonctionnalités
    """
    queryset = Document.objects.filter(is_deleted=False)
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DocumentDetailSerializer
        return DocumentSerializer

    def perform_create(self, serializer):
        """Associe l'utilisateur connecté comme créateur"""
        serializer.save(creator=self.request.user)

    @action(detail=False, methods=['GET'])
    def all(self, request):
        """1.1 All Documents - CORRIGÉ LE NOM"""
        documents = Document.objects.filter(is_deleted=False).order_by('-created_at')
        
        # Filtres optionnels
        category_id = request.query_params.get('category_id')
        if category_id:
            documents = documents.filter(category_id=category_id)
        
        search = request.query_params.get('search')
        if search:
            documents = documents.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(ocr_content__icontains=search)
            )
        
        serializer = self.get_serializer(documents, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def recent(self, request):
        """1.2 Recently Accessed - CORRIGÉ LE NOM"""
        recent_accesses = DocumentAccess.objects.filter(
            user=request.user
        ).select_related('document').order_by('-accessed_at')[:50]
        
        documents = [access.document for access in recent_accesses if not access.document.is_deleted]
        
        # Si pas d'accès récents, retourner les documents récemment créés
        if not documents:
            seven_days_ago = timezone.now() - timedelta(days=7)
            documents = Document.objects.filter(
                created_at__gte=seven_days_ago,
                is_deleted=False
            ).order_by('-created_at')[:20]
        
        serializer = self.get_serializer(documents, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def created(self, request):
        """1.3 Recently Created - CORRIGÉ LE NOM"""
        thirty_days_ago = timezone.now() - timedelta(days=30)
        documents = Document.objects.filter(
            created_at__gte=thirty_days_ago,
            is_deleted=False
        ).order_by('-created_at')[:100]
        
        serializer = self.get_serializer(documents, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def favorites(self, request):
        """1.4 Documents favoris"""
        documents = Document.objects.filter(
            is_favorite=True,
            is_deleted=False
        ).order_by('-created_at')
        
        serializer = self.get_serializer(documents, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def toggle_favorite(self, request, pk=None):
        """Basculer le statut favori d'un document"""
        document = self.get_object()
        document.is_favorite = not document.is_favorite
        document.save()
        
        return Response({
            'is_favorite': document.is_favorite,
            'message': 'Ajouté aux favoris' if document.is_favorite else 'Retiré des favoris'
        })

    @action(detail=False, methods=['GET'])
    def trash(self, request):
        """1.5 Corbeille"""
        documents = Document.objects.filter(
            is_deleted=True
        ).order_by('-deleted_at')
        
        serializer = self.get_serializer(documents, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def soft_delete(self, request, pk=None):
        """Supprimer un document (soft delete)"""
        document = self.get_object()
        document.soft_delete(request.user)
        
        return Response({
            'message': 'Document déplacé vers la corbeille',
            'deleted_at': document.deleted_at
        })

    @action(detail=True, methods=['POST'])
    def restore(self, request, pk=None):
        """Restaurer un document depuis la corbeille"""
        document = get_object_or_404(Document, pk=pk, is_deleted=True)
        
        if not document.can_be_restored:
            return Response(
                {'error': 'Ce document ne peut plus être restauré (> 30 jours)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        document.restore_from_trash()
        return Response({'message': 'Document restauré avec succès'})

    @action(detail=True, methods=['GET'])
    def download(self, request, pk=None):
        """Télécharger la dernière version d'un document"""
        document = self.get_object()
        
        # Marquer comme consulté
        document.mark_as_accessed(request.user)
        
        try:
            latest_version = document.versions.latest('version_number')
            file_path = os.path.join(settings.MEDIA_ROOT, latest_version.file_path)
            
            if os.path.exists(file_path):
                response = FileResponse(
                    open(file_path, 'rb'),
                    as_attachment=True,
                    filename=document.original_filename or f"{document.title}.pdf"
                )
                return response
            else:
                return Response(
                    {'error': 'Fichier introuvable'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        except DocumentVersion.DoesNotExist:
            return Response(
                {'error': 'Aucune version trouvée'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['GET'])
    def search(self, request):
        """8.1-8.2 Recherche dans les documents"""
        query = request.query_params.get('q', '')
        
        if not query:
            return Response(
                {'error': 'Paramètre de recherche requis'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Recherche dans titre, description et contenu OCR
        documents = Document.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(ocr_content__icontains=query),
            is_deleted=False
        )
        
        # Filtres avancés
        category_id = request.query_params.get('category_id')
        if category_id:
            documents = documents.filter(category_id=category_id)
        
        date_from = request.query_params.get('date_from')
        if date_from:
            documents = documents.filter(created_at__gte=date_from)
        
        date_to = request.query_params.get('date_to')
        if date_to:
            documents = documents.filter(created_at__lte=date_to)
        
        serializer = self.get_serializer(documents, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """1.7 Créer un nouveau document avec upload de fichier"""
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
                
                # Calcul du hash pour détection de doublons
                file_obj.seek(0)
                file_content = file_obj.read()
                file_hash = hashlib.sha256(file_content).hexdigest()
                file_obj.seek(0)
                
                # Créer le répertoire pour ce document
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
                
                # Mettre à jour le document avec les infos du fichier
                document.file_hash = file_hash
                document.file_size = file_obj.size
                document.mime_type = file_obj.content_type
                document.original_filename = file_obj.name
                document.save()
                
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


@api_view(['GET'])
def dashboard_stats(request):
    """Statistiques pour le dashboard"""
    try:
        stats = {
            'total_documents': Document.objects.filter(is_deleted=False).count(),
            'recent_documents': Document.objects.filter(
                created_at__gte=timezone.now() - timedelta(days=7),
                is_deleted=False
            ).count(),
            'favorites_count': Document.objects.filter(
                is_favorite=True, 
                is_deleted=False
            ).count(),
            'trash_count': Document.objects.filter(is_deleted=True).count(),
            'total_users': User.objects.filter(is_active=True).count(),
            'storage_used': Document.objects.aggregate(
                total_size=Sum('file_size')
            )['total_size'] or 0,
        }
        
        return Response(stats)
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )