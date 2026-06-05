from django.contrib import admin
from .models import Announcement  # Importation du modèle Announcement pour l'enregistrer

# ==========================================
# CONFIGURATION DE L'ADMINISTRATION DES ANNONCES
# ==========================================

# Décorateur officiel pour enregistrer et lier le modèle Announcement à sa classe de configuration admin
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    # Colonnes affichées dans le tableau récapitulatif de la liste des annonces
    list_display = ('title', 'category', 'date_published', 'is_active')
    
    # Filtres rapides disponibles dans le volet latéral droit (filtrage par catégorie ou statut d'activation)
    list_filter = ('category', 'is_active')
    
    # Barre de recherche permettant de filtrer les annonces par des mots-clés présents dans le titre ou le contenu
    search_fields = ('title', 'content')
