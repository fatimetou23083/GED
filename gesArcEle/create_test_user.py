import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gesArcEle.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

# Créer un utilisateur de test s'il n'existe pas déjà
username = 'sara'
password = '123456'

try:
    user = User.objects.get(username=username)
    print(f"L'utilisateur {username} existe déjà.")
except User.DoesNotExist:
    user = User.objects.create_user(username=username, password=password)
    print(f"Utilisateur {username} créé avec succès.")

# Créer ou récupérer un token pour cet utilisateur
token, created = Token.objects.get_or_create(user=user)
print(f"Token pour {username}: {token.key}")
print(f"Utilisez ce header dans vos requêtes: Authorization: Token {token.key}")