# gesArcEle/urls.py - VERSION CORRIGÉE
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # Administration Django
    path('admin/', admin.site.urls),
    
    # Authentification
    path('api/auth/token/', obtain_auth_token, name='api_token_auth'),
    
    # APIs des applications
    path('api/archive/', include('archive.urls')),
    path('api/users/', include('users.urls')),
    path('api/catalog/', include('Catalog.urls')),
    path('api/documents/', include('documents.urls')),
    path('api/permissions/', include('permissions.urls')),
    path('api/tags/', include('Tagger.urls')),
    path('api/comments/', include('commentaires.urls')),
    path('api/cabinets/', include('cabinets.urls')),
    path('api/metadata/', include('metadata.urls')),
    path('api/workflows/', include('workflows.urls')),
    path('api/messaging/', include('messaging.urls')),
    path('api/indexing/', include('indexing.urls')),
    path('api/settings/', include('settings.urls')),
]

# Servir les fichiers media et static en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)