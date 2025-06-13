"""
URL configuration for gesArcEle project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.authtoken import views as auth_token_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('archive.urls')),
    path('api/',include('users.urls')),
    path('api/',include('Catalog.urls')),
    path('api/',include('documents.urls')),
    path('api/',include('permissions.urls')),
    path('api/',include('Tagger.urls')),
    path('api/',include('commentaires.urls')),
    path('api/token/', obtain_auth_token),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Ajout des URLs pour servir les fichiers statiques en développement
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
