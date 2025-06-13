from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer, CategoryTreeSerializer
class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les catégories du catalogue
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtre les catégories selon les paramètres"""
        queryset = Category.objects.all()
        
        # Filtre par catégorie parente
        parent_id = self.request.query_params.get('parent_id', None)
        if parent_id:
            if parent_id == 'null':  # Pour récupérer les catégories racines
                queryset = queryset.filter(parent_id__isnull=True)
            else:
                queryset = queryset.filter(parent_id=parent_id)
        
        return queryset
    
    def get_serializer_class(self):
        """Détermine le sérialiseur à utiliser"""
        if self.action == 'tree':
            return CategoryTreeSerializer
        return CategorySerializer
    
    @action(detail=False, methods=['get'])
    def root_categories(self, request):
        """Récupère les catégories racines (sans parent)"""
        categories = Category.objects.filter(parent_id__isnull=True)
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def subcategories(self, request, pk=None):
        """Récupère les sous-catégories d'une catégorie"""
        category = self.get_object()
        subcategories = Category.objects.filter(parent_id=category.id)
        serializer = self.get_serializer(subcategories, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def documents(self, request, pk=None):
        """Récupère les documents d'une catégorie"""
        category = self.get_object()
        
        # Import ici pour éviter les problèmes d'importation circulaire
        from documents.models import Document
        from documents.serializers import DocumentSerializer
        
        documents = Document.objects.filter(category_id=category.id)
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def hierarchy(self, request, pk=None):
        """Récupère la hiérarchie complète d'une catégorie (parents)"""
        category = self.get_object()
        hierarchy = []
        
        # Remonte la hiérarchie jusqu'à la racine
        current = category
        while current:
            hierarchy.insert(0, {
                'id': current.id,
                'name': current.name,
                'description': current.description
            })
            if current.parent_id:
                current = current.parent_id
            else:
                break
        
        return Response(hierarchy)
    
    @action(detail=False, methods=['get'])
    def tree(self, request):
        """Récupère l'arborescence complète des catégories"""
        root_categories = Category.objects.filter(parent_id__isnull=True)
        serializer = CategoryTreeSerializer(root_categories, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def move(self, request):
        """Déplace une catégorie vers un nouveau parent"""
        category_id = request.data.get('category_id')
        new_parent_id = request.data.get('new_parent_id')
        
        if not category_id:
            return Response({"error": "Le paramètre category_id est requis"}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        category = get_object_or_404(Category, id=category_id)
        
        # Si new_parent_id est None ou "null", on déplace à la racine
        if new_parent_id in [None, "null"]:
            category.parent_id = None
        else:
            new_parent = get_object_or_404(Category, id=new_parent_id)
            
            # Vérifie qu'on ne crée pas de cycle dans la hiérarchie
            parent_check = new_parent
            while parent_check:
                if parent_check.id == category.id:
                    return Response({"error": "Impossible de créer un cycle dans la hiérarchie"}, 
                                   status=status.HTTP_400_BAD_REQUEST)
                parent_check = parent_check.parent_id
            
            category.parent_id = new_parent
        
        category.save()
        serializer = self.get_serializer(category)
        return Response(serializer.data)