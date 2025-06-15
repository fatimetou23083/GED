# users/views.py - Version corrigée
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db.models import Q
from rest_framework import viewsets, status, permissions, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
import base64
import uuid
import os
from django.conf import settings

from .models import User, Profile
from .serializers import (
    UserSerializer, 
    UserLoginSerializer, 
    UserRegisterSerializer, 
    ProfileSerializer,
    UserWithProfileSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les utilisateurs
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['login', 'register']:
            return [permissions.AllowAny()]
        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'list_with_profiles']:
            return UserWithProfileSerializer
        return UserSerializer
    
    def get_queryset(self):
        """Optimiser les requêtes avec select_related"""
        if self.action in ['list', 'retrieve', 'list_with_profiles']:
            return User.objects.select_related('profile').all()
        return super().get_queryset()
    
    @action(detail=False, methods=['get'])
    def list_with_profiles(self, request):
        """Récupérer tous les utilisateurs avec leurs profils"""
        users = User.objects.select_related('profile').all()
        
        # Créer les profils manquants
        for user in users:
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user)
        
        # Récupérer à nouveau avec les profils créés
        users = User.objects.select_related('profile').all()
        serializer = UserWithProfileSerializer(users, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Rechercher des utilisateurs"""
        query = request.query_params.get('q', '')
        if not query:
            return Response({"error": "Le paramètre 'q' est requis"}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        users = User.objects.select_related('profile').filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(profile__job_title__icontains=query) |
            Q(profile__department__icontains=query)
        )
        
        serializer = UserWithProfileSerializer(users, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statistiques des utilisateurs"""
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        inactive_users = total_users - active_users
        
        # Statistiques par département
        departments = Profile.objects.exclude(
            department__isnull=True
        ).exclude(
            department__exact=''
        ).values_list('department', flat=True)
        
        dept_stats = {}
        for dept in departments:
            dept_stats[dept] = Profile.objects.filter(department=dept).count()
        
        return Response({
            'total_users': total_users,
            'active_users': active_users,
            'inactive_users': inactive_users,
            'users_by_department': dept_stats
        })
    
    @action(detail=True, methods=['patch'])
    def toggle_status(self, request, pk=None):
        """Activer/désactiver un utilisateur (admin seulement)"""
        if not request.user.is_staff:
            return Response({"error": "Permission refusée"}, 
                           status=status.HTTP_403_FORBIDDEN)
        
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        
        serializer = UserWithProfileSerializer(user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """Connexion avec email + mot de passe"""
        # IMPORTANT: Permettre l'accès sans authentification
        self.permission_classes = [permissions.AllowAny]
        
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {'error': 'Email invalide'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # CORRECTION: Ajouter 'request' comme premier paramètre
            user = authenticate(request, username=user_obj.username, password=password)
            
            if user and user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                })
            else:
                return Response(
                    {'error': 'Mot de passe incorrect ou compte inactif'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """Enregistrer un nouvel utilisateur"""
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                # Créer le profil avec données si fournies
                Profile.objects.create(
                    user=user,
                    avatar=request.data.get("avatar", ""),
                    job_title=request.data.get("job_title", ""),
                    department=request.data.get("department", "")
                )

                # Créer le token
                token = Token.objects.create(user=user)
                return Response({
                    'token': token.key,
                    'user_id': user.id,
                    'message': 'Utilisateur créé avec succès'
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les profils d'utilisateurs
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user_id = self.request.data.get("user_id")
        
        if user_id and self.request.user.is_staff:
            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                raise serializers.ValidationError("L'utilisateur spécifié n'existe pas.")
            serializer.save(user=user)
        else:
            serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)

    @action(detail=False, methods=['get', 'put', 'patch'])
    def my_profile(self, request):
        """Récupérer ou mettre à jour le profil de l'utilisateur connecté"""
        try:
            profile = Profile.objects.get(user=request.user)
            
            if request.method == 'GET':
                serializer = self.get_serializer(profile)
                return Response(serializer.data)
            
            # Pour PUT et PATCH
            serializer = self.get_serializer(profile, data=request.data, partial=request.method=='PATCH')
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
            
        except Profile.DoesNotExist:
            if request.method == 'GET':
                return Response({'error': 'Profil non trouvé'}, status=status.HTTP_404_NOT_FOUND)
            
            # Si le profil n'existe pas et c'est une requête PUT/PATCH, créez-le
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def upload_avatar(self, request):
        """Upload d'avatar - support FormData et base64"""
        try:
            profile, created = Profile.objects.get_or_create(user=request.user)
            
            # Méthode 1: Upload via FormData
            if 'avatar' in request.FILES:
                avatar_file = request.FILES['avatar']
                
                # Validation du fichier
                if avatar_file.size > 5 * 1024 * 1024:  # 5MB max
                    return Response({"error": "Fichier trop volumineux (max 5MB)"}, 
                                   status=status.HTTP_400_BAD_REQUEST)
                
                # Vérifier le type MIME
                allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
                if avatar_file.content_type not in allowed_types:
                    return Response({"error": "Type de fichier non autorisé"}, 
                                   status=status.HTTP_400_BAD_REQUEST)
                
                # Générer un nom de fichier unique
                ext = os.path.splitext(avatar_file.name)[1]
                filename = f"avatars/{uuid.uuid4()}{ext}"
                
                # Sauvegarder le fichier
                file_path = default_storage.save(filename, ContentFile(avatar_file.read()))
                
                # Mettre à jour le profil
                profile.avatar = file_path
                profile.save()
                
                # Construire l'URL complète
                file_url = request.build_absolute_uri(settings.MEDIA_URL + file_path)
                
                return Response({
                    'url': file_url,
                    'id': str(profile.id)
                })
            
            # Méthode 2: Upload via base64
            elif 'avatar_base64' in request.data:
                try:
                    # Décoder l'image base64
                    format, imgstr = request.data['avatar_base64'].split(';base64,')
                    ext = format.split('/')[-1]
                    
                    # Générer un nom de fichier unique
                    filename = f"avatars/{uuid.uuid4()}.{ext}"
                    
                    # Sauvegarder le fichier
                    data = ContentFile(base64.b64decode(imgstr))
                    file_path = default_storage.save(filename, data)
                    
                    # Mettre à jour le profil
                    profile.avatar = file_path
                    profile.save()
                    
                    # Construire l'URL complète
                    file_url = request.build_absolute_uri(settings.MEDIA_URL + file_path)
                    
                    return Response({
                        'url': file_url,
                        'id': str(profile.id)
                    })
                    
                except Exception as e:
                    return Response({
                        'error': 'Erreur lors du décodage de l\'image base64',
                        'details': str(e)
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                return Response({
                    'error': 'Aucun fichier fourni'
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({
                'error': 'Erreur lors de l\'upload',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)