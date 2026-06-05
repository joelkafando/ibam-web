from django.shortcuts import render, get_object_or_404
from .models import Announcement

# ==========================================
# VUE : LISTE DES ANNONCES PUBLIQUES
# ==========================================
def announcement_list(request):
    """
    Récupère toutes les annonces marquées comme actives en base de données 
    et les transmet sous forme de liste au template dédié.
    """
    # Extraction et filtrage : on ne récupère que les annonces dont 'is_active' est égal à True
    announcements = Announcement.objects.filter(is_active=True)
    
    # Rendu graphique de la page principale des annonces avec injection de la liste
    return render(request, 'announcements/announcements.html', {'announcements': announcements})


# ==========================================
# VUE : DÉTAIL D'UNE ANNONCE SPÉCIFIQUE
# ==========================================
def announcement_detail(request, pk):
    """
    Charge une annonce unique à partir de son identifiant numérique (clé primaire 'pk').
    Renvoie une erreur 404 standard si l'annonce n'existe pas ou a été supprimée.
    """
    # Recherche sécurisée de l'objet ou levée immédiate d'une exception HTTP 404 Page introuvable
    announcement = get_object_or_404(Announcement, pk=pk)
    
    # Rendu graphique de l'annonce seule pour une lecture complète de son contenu
    return render(request, 'announcements/announcement_detail.html', {'announcement': announcement})
