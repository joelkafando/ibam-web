"""
Configuration globale des URLs du projet d'établissement (config).
Centralise et distribue les préfixes de chemins vers les modules métiers de l'application.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ==========================================================================
    # 1. ADMINISTRATION TECHNIQUE CENTRALE
    # ==========================================================================
    # Point d'accès au panneau de gestion natif de Django (Back-Office technique)
    path('admin/', admin.site.urls),
    
    # ==========================================================================
    # 2. ESPACES PUBLICS ET COMMUNICANTS (VITRINE)
    # ==========================================================================
    # Racine du site : englobe les pages statiques et éditoriales de base (Accueil, Contact, etc.)
    path('', include('core.urls')), 
    
    # Module des actualités : utilise un tuple pour forcer la configuration de l'espace de noms (namespace) et • namespace='announcements' permet d'utiliser {% url 'announcements:...' %} dans les templates.
    path('announcements/', include(('announcements.urls', 'announcements'), namespace='announcements')),
    
    # ==========================================================================
    # 3. INTERFACES CONNECTÉES ET LOGIQUE MÉTIER ACADÉMIQUE (INTRANET)
    # ==========================================================================
    # Passerelle d'authentification : prend en charge les flux d'inscription et de connexion
    path('accounts/', include('accounts.urls')),
    
    # Espace de travail : distribue l'accès vers les 3 types de tableaux de bord (Rôles RBAC)
    path('dashboard/', include('dashboard.urls')),

    # Gestion de la scolarité : centralise les données des filières et des grilles d'emplois du temps
    path('academics/', include('academics.urls')), 
    #Il s'agit du forum de L'application
    path('forum/', include('forum.urls')),

]

# ==========================================================================
# 4. SERVEUR DE FICHIERS MÉDIAS ET PIÈCES JOINTES (MODE LOGOCAL)
# ==========================================================================
# Ajout des routes statiques pour le chargement des images ou documents PDF vers le dossier MEDIA_ROOT.
# Condition sécurisée : s'active exclusivement lorsque le mode de débogage (DEBUG=True) est actif en développement.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
