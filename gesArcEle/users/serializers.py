# users/serializers.py - Version corrigée complète
from rest_framework import serializers
from .models import User, Profile

class UserSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les utilisateurs"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active']
        read_only_fields = ['id', 'is_active', 'is_superuser']

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class UserRegisterSerializer(serializers.ModelSerializer):
    """Sérialiseur pour l'inscription"""
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate(self, data):
        """Vérifie que les mots de passe correspondent"""
        if data['password'] != data.pop('password_confirm'):
            raise serializers.ValidationError("Les mots de passe ne correspondent pas")
        return data
    
    def create(self, validated_data):
        """Crée et retourne un nouvel utilisateur"""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user_id', 'avatar', 'job_title', 'department']
        read_only_fields = ['id', 'user_id']

class UserWithProfileSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les utilisateurs avec leurs profils"""
    profile = ProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'is_active', 'is_superuser', 'date_joined', 'profile']