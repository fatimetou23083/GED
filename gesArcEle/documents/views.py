# documents/views.py - MÉTHODE CREATE COMPLÈTE ET CORRIGÉE
import os
import mimetypes
from django.conf import settings
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from Catalog.models import Category  
from documents.models import Document, DocumentVersion, Metadata
from .serializers import DocumentSerializer, DocumentVersionSerializer, MetadataSerializer, DocumentDetailSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    """Point d'entrée API pour gérer les documents"""
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        """Exclure les documents supprimés par défaut"""
        return Document.objects.filter(is_deleted=False)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DocumentDetailSerializer
        return DocumentSerializer

    def perform_create(self, serializer):
        """Associe l'utilisateur connecté comme créateur du document"""
        serializer.save(creator=self.request.user)

    def create(self, request, *args, **kwargs):
        """✅ CRÉER UN NOUVEAU DOCUMENT AVEC UPLOAD - VERSION COMPLÈTE"""
        try:
            print(f"📥 === DÉBUT UPLOAD ===")
            print(f"📥 Headers: {dict(request.headers)}")
            print(f"📥 Method: {request.method}")
            print(f"📥 Content-Type: {request.content_type}")
            print(f"📥 User: {request.user}")
            print(f"📥 Data keys: {list(request.data.keys())}")
            print(f"📥 Files keys: {list(request.FILES.keys())}")
            
            # ✅ 1. VALIDATION DES DONNÉES OBLIGATOIRES
            title = request.data.get('title', '').strip()
            if not title:
                return Response(
                    {"error": "Le titre est requis"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if len(title) < 3:
                return Response(
                    {"error": "Le titre doit contenir au moins 3 caractères"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            category_id = request.data.get('category_id')
            if not category_id:
                return Response(
                    {"error": "La catégorie est requise"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # ✅ 2. VÉRIFICATION DE LA CATÉGORIE
            try:
                category_id = int(category_id)
                category = Category.objects.get(id=category_id)
                print(f"✅ Catégorie trouvée: {category.name}")
            except (ValueError, Category.DoesNotExist):
                return Response(
                    {"error": f"Catégorie invalide: {category_id}"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # ✅ 3. VÉRIFICATION DU FICHIER
            if 'file' not in request.FILES:
                return Response(
                    {"error": "Aucun fichier fourni"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            file_obj = request.FILES['file']
            print(f"📎 Fichier reçu: {file_obj.name}")
            print(f"📎 Taille: {file_obj.size} bytes")
            print(f"📎 Type MIME: {file_obj.content_type}")
            
            # ✅ 4. VALIDATION DE LA TAILLE (50MB max)
            max_size = 50 * 1024 * 1024  # 50MB
            if file_obj.size > max_size:
                return Response(
                    {"error": f"Fichier trop volumineux ({file_obj.size} bytes). Maximum: 50MB"}, 
                    status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
                )
            
            # ✅ 5. VALIDATION DU TYPE MIME
            allowed_types = [
                'application/pdf',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/vnd.ms-excel',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'application/vnd.ms-powerpoint',
                'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                'image/jpeg',
                'image/png',
                'image/jpg'
            ]
            
            file_mime_type = file_obj.content_type
            if file_mime_type not in allowed_types:
                # Vérification supplémentaire par extension si MIME non reconnu
                file_ext = os.path.splitext(file_obj.name)[1].lower()
                ext_to_mime = {
                    '.pdf': 'application/pdf',
                    '.doc': 'application/msword',
                    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                    '.xls': 'application/vnd.ms-excel',
                    '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    '.ppt': 'application/vnd.ms-powerpoint',
                    '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                    '.jpg': 'image/jpeg',
                    '.jpeg': 'image/jpeg',
                    '.png': 'image/png'
                }
                
                if file_ext not in ext_to_mime:
                    return Response(
                        {"error": f"Type de fichier non supporté: {file_mime_type} (extension: {file_ext})"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Utiliser le MIME type basé sur l'extension
                file_mime_type = ext_to_mime[file_ext]
                print(f"📎 Type MIME corrigé: {file_mime_type}")
            
            # ✅ 6. CRÉATION DU DOCUMENT
            description = request.data.get('description', '').strip()
            document_status = request.data.get('status', 'DRAFT')
            
            document = Document.objects.create(
                title=title,
                description=description,
                category=category,
                status=document_status,
                creator=request.user
            )
            
            print(f"✅ Document créé avec ID: {document.id}")
            
            # ✅ 7. SAUVEGARDE DU FICHIER
            try:
                # Créer le répertoire pour ce document
                document_dir = os.path.join(settings.MEDIA_ROOT, 'documents', str(document.id))
                os.makedirs(document_dir, exist_ok=True)
                print(f"📁 Répertoire créé: {document_dir}")
                
                # Générer un nom de fichier sécurisé
                file_ext = os.path.splitext(file_obj.name)[1]
                safe_filename = f"document_{document.id}_v1{file_ext}"
                file_path = os.path.join(document_dir, safe_filename)
                relative_path = os.path.join('documents', str(document.id), safe_filename)
                
                # Écrire le fichier
                with open(file_path, 'wb+') as destination:
                    for chunk in file_obj.chunks():
                        destination.write(chunk)
                
                print(f"💾 Fichier sauvegardé: {file_path}")
                
                # ✅ 8. CRÉER LA VERSION DU DOCUMENT
                version = DocumentVersion.objects.create(
                    document=document,
                    version_number=1,
                    file_path=relative_path,
                    created_by=request.user
                )
                
                print(f"✅ Version créée: v{version.version_number}")
                
                # ✅ 9. CALCULER LE HASH (automatique via le signal dans le modèle)
                document.save()  # Déclenche le calcul du hash
                
            except Exception as file_error:
                print(f"❌ Erreur sauvegarde fichier: {str(file_error)}")
                # Nettoyer en cas d'erreur
                document.delete()
                return Response(
                    {"error": f"Erreur lors de la sauvegarde du fichier: {str(file_error)}"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # ✅ 10. RÉPONSE DE SUCCÈS
            serializer = self.get_serializer(document)
            response_data = serializer.data
            
            print(f"✅ === UPLOAD TERMINÉ AVEC SUCCÈS ===")
            print(f"✅ Document ID: {document.id}")
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(f"❌ === ERREUR GÉNÉRALE ===")
            print(f"❌ Type d'erreur: {type(e).__name__}")
            print(f"❌ Message: {str(e)}")
            import traceback
            traceback.print_exc()
            
            return Response(
                {"error": f"Erreur serveur inattendue: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # ✅ MÉTHODE POUR TÉLÉCHARGER LA DERNIÈRE VERSION
    @action(detail=True, methods=['get'])
    def download_latest(self, request, pk=None):
        """Télécharger la dernière version du document"""
        document = self.get_object()
        try:
            latest_version = document.versions.latest('version_number')
            file_path = os.path.join(settings.MEDIA_ROOT, latest_version.file_path)
            
            if os.path.exists(file_path):
                response = FileResponse(
                    open(file_path, 'rb'),
                    as_attachment=True,
                    filename=os.path.basename(file_path)
                )
                return response
            else:
                return Response(
                    {"error": "Fichier non trouvé sur le disque"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        except DocumentVersion.DoesNotExist:
            return Response(
                {"error": "Aucune version trouvée pour ce document"}, 
                status=status.HTTP_404_NOT_FOUND
            )

# ✅ AJOUT DANS DocumentVersionViewSet
class DocumentVersionViewSet(viewsets.ModelViewSet):
    """API endpoint pour gérer les versions de documents"""
    queryset = DocumentVersion.objects.all()
    serializer_class = DocumentVersionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """✅ TÉLÉCHARGER UNE VERSION SPÉCIFIQUE"""
        version = self.get_object()
        file_path = os.path.join(settings.MEDIA_ROOT, version.file_path)
        
        if os.path.exists(file_path):
            response = FileResponse(
                open(file_path, 'rb'),
                as_attachment=True,
                filename=os.path.basename(file_path)
            )
            return response
        
        return Response(
            {"error": "Fichier non trouvé"},
            status=status.HTTP_404_NOT_FOUND
        )