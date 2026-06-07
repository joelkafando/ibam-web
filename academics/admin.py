# Importation du module admin de Django pour gérer l'interface d'administration
from django.contrib import admin

# Importation des modèles Filiere et EmploiDuTemps depuis le fichier models.py local
from .models import Filiere, EmploiDuTemps

# Importation des modèles RessourcePedagogique et DisponibiliteEnseignant depuis models.py
from .models import RessourcePedagogique, DisponibiliteEnseignant


# ==========================================
# 1. CONFIGURATION DE L'ADMINISTRATION DES FILIÈRES
# ==========================================

# Décorateur Django qui enregistre automatiquement le modèle Filiere
# dans le site d'administration en associant la classe FiliereAdmin
@admin.register(Filiere)

# Définition de la classe d'administration pour le modèle Filiere
# Elle hérite de admin.ModelAdmin qui fournit les fonctionnalités de base
class FiliereAdmin(admin.ModelAdmin):

    # Définit les colonnes visibles dans la liste des filières dans l'admin
    # Ici : le nom de la filière, son niveau et sa durée
    list_display = ('nom_filiere', 'niveau', 'duree')

    # Active la barre de recherche dans l'admin et cible le champ 'nom_filiere'
    # L'administrateur pourra rechercher une filière par son nom
    search_fields = ('nom_filiere',)


# ==========================================
# 2. CONFIGURATION DE L'ADMINISTRATION DES EMPLOIS DU TEMPS
# ==========================================

# Décorateur Django qui enregistre le modèle EmploiDuTemps dans l'admin
# La classe EmploiDuTempsAdmin définit l'affichage et les options de gestion
@admin.register(EmploiDuTemps)

# Définition de la classe d'administration pour le modèle EmploiDuTemps
class EmploiDuTempsAdmin(admin.ModelAdmin):

    # Liste des colonnes affichées dans le tableau de bord de l'admin
    # Chaque élément correspond à un champ du modèle EmploiDuTemps
    list_display = (
        'filiere',       # La filière concernée par le cours
        'niveau_etude',  # Le niveau d'études (ex: L1, L2, M1...)
        'semaine_du',    # La date de début de la semaine concernée
        'nom_matiere',   # Le nom de la matière enseignée
        'enseignant',    # L'enseignant responsable du cours
        'jour',          # Le jour de la semaine du cours
        'heure_debut',   # L'heure de début du cours
        'heure_fin',     # L'heure de fin du cours
        'salle'          # La salle où se déroule le cours
    )

    # Panneau de filtres latéral permettant de filtrer la liste
    # par filière, niveau d'étude, jour de la semaine ou semaine
    list_filter = ('filiere', 'niveau_etude', 'jour', 'semaine_du')

    # Champs sur lesquels porte la recherche textuelle dans l'admin
    # Permet de rechercher par nom de matière, enseignant ou salle
    search_fields = ('nom_matiere', 'enseignant', 'salle')

    # Définit la mise en page du formulaire d'ajout/modification
    # Les champs sont regroupés en sections nommées pour plus de clarté
    fieldsets = (

        # Première section nommée "Informations Générales"
        # Regroupe les champs liés au contexte académique du cours
        ('Informations Générales', {
            'fields': ('filiere', 'niveau_etude', 'semaine_du', 'nom_matiere', 'enseignant')
            #           ^ filière  ^ niveau        ^ semaine      ^ matière       ^ enseignant
        }),

        # Deuxième section nommée "Planification Horaire"
        # Regroupe les champs liés à la logistique temporelle et spatiale
        ('Planification Horaire', {
            'fields': ('jour', 'heure_debut', 'heure_fin', 'salle')
            #           ^ jour   ^ début         ^ fin        ^ salle
        }),
    )


# ==========================================
# 3. ENREGISTREMENT DE LA BIBLIOTHÈQUE
# ==========================================

# Décorateur qui enregistre le modèle RessourcePedagogique dans l'admin
@admin.register(RessourcePedagogique)

# Classe d'administration pour la gestion des ressources pédagogiques
class RessourcePedagogiqueAdmin(admin.ModelAdmin):

    # Colonnes affichées dans la liste : titre, enseignant, filière, niveau et date de dépôt
    list_display = ('titre_cours', 'enseignant', 'filiere', 'niveau_etude', 'date_depot')

    # Filtres latéraux permettant de trier les ressources par filière ou niveau d'étude
    list_filter = ('filiere', 'niveau_etude')

    # Recherche activée sur le titre du cours et le nom d'utilisateur de l'enseignant
    # '__username' accède au champ username de l'objet lié enseignant (relation ForeignKey)
    search_fields = ('titre_cours', 'enseignant__username')


# Décorateur qui enregistre le modèle DisponibiliteEnseignant dans l'admin
@admin.register(DisponibiliteEnseignant)

# Classe d'administration pour gérer les disponibilités des enseignants
class DisponibiliteEnseignantAdmin(admin.ModelAdmin):

    # Colonnes affichées : enseignant concerné, jour, période et date de soumission
    list_display = ('enseignant', 'jour', 'periode', 'date_soumission')

    # Filtres latéraux pour trier les disponibilités par jour ou par période
    list_filter = ('jour', 'periode')

    # Recherche activée sur le nom d'utilisateur de l'enseignant et ses notes complémentaires
    # '__username' traverse la relation ForeignKey pour accéder au champ username
    search_fields = ('enseignant__username', 'note_complementaire')