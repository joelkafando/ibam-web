from django.contrib import admin
from .models import Filiere, EmploiDuTemps
from .models import RessourcePedagogique, DisponibiliteEnseignant

# ==========================================
# 1. CONFIGURATION DE L'ADMINISTRATION DES FILIÈRES
# ==========================================

# Décorateur pour enregistrer le modèle Filiere dans le site d'administration
@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    # Colonnes affichées dans la liste récapitulative des filières
    list_display = ('nom_filiere', 'niveau', 'duree')
    
    # Barre de recherche basée sur le nom de la filière
    search_fields = ('nom_filiere',)


# ==========================================
# 2. CONFIGURATION DE L'ADMINISTRATION DES EMPLOIS DU TEMPS
# ==========================================

# Décorateur pour enregistrer le modèle EmploiDuTemps dans le site d'administration
@admin.register(EmploiDuTemps)
class EmploiDuTempsAdmin(admin.ModelAdmin):
    # Colonnes affichées dans le tableau récapitulatif des emplois du temps
    list_display = (
        'filiere', 
        'niveau_etude', 
        'semaine_du', 
        'nom_matiere', 
        'enseignant', 
        'jour', 
        'heure_debut', 
        'heure_fin', 
        'salle'
    )
    
    # Filtres disponibles dans le panneau latéral droit pour trier rapidement les données
    list_filter = ('filiere', 'niveau_etude', 'jour', 'semaine_du')
    
    # Barre de recherche permettant de filtrer par matière, enseignant ou salle
    search_fields = ('nom_matiere', 'enseignant', 'salle')
    
    # Organisation visuelle du formulaire d'ajout et de modification (regroupement par sections)
    fieldsets = (
        # Première section : Détails académiques et contextuels
        ('Informations Générales', {
            'fields': ('filiere', 'niveau_etude', 'semaine_du', 'nom_matiere', 'enseignant')
        }),
        # Deuxième section : Détails logistiques et temporels
        ('Planification Horaire', {
            'fields': ('jour', 'heure_debut', 'heure_fin', 'salle')
        }),
    )

# ==========================================
# 3. ENREGISTREMENT DE LA BIBLIOTHÈQUE
# ==========================================
@admin.register(RessourcePedagogique)
class RessourcePedagogiqueAdmin(admin.ModelAdmin):
    list_display = ('titre_cours', 'enseignant', 'filiere', 'niveau_etude', 'date_depot')
    list_filter = ('filiere', 'niveau_etude')
    search_fields = ('titre_cours', 'enseignant__username')

@admin.register(DisponibiliteEnseignant)
class DisponibiliteEnseignantAdmin(admin.ModelAdmin):
    list_display = ('enseignant', 'jour', 'periode', 'date_soumission')
    list_filter = ('jour', 'periode')
    search_fields = ('enseignant__username', 'note_complementaire')