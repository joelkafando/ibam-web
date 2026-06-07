# Importation du module models de Django pour définir les champs et le comportement du modèle
from django.db import models


# ==========================================
# MODÈLE : PAGE INSTITUTIONNELLE
# ==========================================

# Définition du modèle PageInstitutionnelle qui hérite de models.Model (classe de base Django)
# Chaque instance correspond à une page de présentation statique de l'établissement
# Fonctionne comme un mini-CMS : l'administrateur édite le contenu sans toucher au code source
class PageInstitutionnelle(models.Model):
    """
    Modèle gérant le contenu éditorial des pages de présentation de l'établissement.
    Fonctionne comme un mini-CMS basé sur un code de page unique pour lier le contenu aux templates.
    """

    # Liste de tuples définissant les pages institutionnelles gérables par ce modèle
    # Format : ('code_technique_stocké_en_BDD', 'Label lisible affiché dans l'interface admin')
    # Chaque code correspond à une route/vue Django spécifique dans urls.py et views.py
    CODE_PAGES = [
        ('PRESENTATION', 'Présentation & Missions'), # Page de présentation générale de l'établissement
        ('HISTORIQUE', 'Historique'),                # Page retraçant l'histoire de l'établissement
        ('EQUIPE', 'Équipe Dirigeante'),             # Page présentant les membres de la direction
    ]

    # Champ de sélection servant d'identifiant technique unique pour chaque page institutionnelle
    # max_length=20 : longueur suffisante pour stocker les codes ('PRESENTATION', 'HISTORIQUE', 'EQUIPE')
    # choices=CODE_PAGES : restreint les valeurs possibles à la liste définie ci-dessus (menu déroulant)
    # unique=True : garantit qu'une seule ligne en base de données peut avoir ce code
    #               Empêche par exemple de créer deux fois la page 'HISTORIQUE'
    # verbose_name : label affiché dans l'interface d'administration Django
    code_page = models.CharField(
        max_length=20,
        choices=CODE_PAGES,             # Menu déroulant limité aux trois pages définies dans CODE_PAGES
        unique=True,                    # Contrainte d'unicité : un seul enregistrement par code de page
        verbose_name="Page cible"       # Label affiché dans l'admin et les formulaires ModelForm
    )

    # Champ texte court pour le titre principal (H1) affiché en haut de la page institutionnelle
    # max_length=200 : limite suffisante pour un titre de page sans être trop restrictive
    # verbose_name : label descriptif affiché dans l'interface d'administration
    titre_principal = models.CharField(
        max_length=200,
        verbose_name="Grand Titre de la Page"   # Label explicite indiquant le rôle de ce champ
    )

    # Champ texte court optionnel pour une phrase d'accroche placée sous le titre principal
    # max_length=250 : légèrement plus long que le titre pour permettre une accroche complète
    # blank=True : champ non obligatoire dans les formulaires Django (peut être laissé vide)
    # null=True : valeur NULL autorisée en base de données si aucun sous-titre n'est saisi
    sous_titre = models.CharField(
        max_length=250,
        blank=True,                         # Facultatif côté formulaire : pas d'erreur si vide
        null=True,                          # NULL autorisé en base : une page peut ne pas avoir de sous-titre
        verbose_name="Sous-titre / Accroche" # Label indiquant la double fonction du champ
    )

    # Champ texte long optionnel pour le premier paragraphe de présentation
    # TextField : pas de limite de caractères, adapté aux textes longs et structurés
    # blank=True + null=True : introduction entièrement facultative (certaines pages peuvent l'omettre)
    introduction = models.TextField(
        blank=True,                             # Non obligatoire dans les formulaires
        null=True,                              # NULL autorisé en base si champ non renseigné
        verbose_name="Texte d'introduction"     # Label affiché dans l'admin
    )

    # Champ texte long obligatoire contenant le cœur de l'information éditoriale de la page
    # TextField sans max_length : aucune limite de longueur imposée (texte libre de taille variable)
    # Champ obligatoire (ni blank=True ni null=True) : une page doit toujours avoir un contenu principal
    # help_text : indication contextuelle affichée sous le champ dans le formulaire admin
    contenu_principal = models.TextField(
        verbose_name="Corps du texte / Contenu principal",          # Label explicite dans l'admin
        help_text="Vous pouvez utiliser du texte ou du HTML basique" # Conseil affiché sous le champ
        #           ^ Indique à l'administrateur qu'il peut saisir du HTML pour enrichir le contenu
    )

    # Champ texte long optionnel destiné aux barres latérales (sidebars) ou encadrés complémentaires
    # Permet d'afficher des informations secondaires sans les mélanger au contenu principal
    # blank=True + null=True : bloc additionnel entièrement facultatif selon la structure de la page
    bloc_secondaire = models.TextField(
        blank=True,                                         # Non obligatoire dans les formulaires
        null=True,                                          # NULL autorisé en base si non renseigné
        verbose_name="Bloc d'information complémentaire"    # Label explicite dans l'admin
    )

    # Champ date/heure mis à jour automatiquement à chaque modification de l'enregistrement
    # auto_now=True : Django met à jour ce champ automatiquement à chaque appel de .save()
    # Différence avec auto_now_add : auto_now_add enregistre uniquement à la CRÉATION
    #                                auto_now enregistre à chaque MODIFICATION (UPDATE)
    # Ce champ est automatiquement en lecture seule dans les formulaires (non modifiable manuellement)
    derniere_mise_a_jour = models.DateTimeField(auto_now=True)
    #                                            ^ Mis à jour à chaque .save() sur cet objet

    # Classe interne Meta : configure les options globales d'affichage et de comportement du modèle
    class Meta:
        verbose_name = "Page Institutionnelle"          # Nom singulier affiché dans l'interface admin
        verbose_name_plural = "Pages Institutionnelles" # Nom pluriel affiché dans l'interface admin
        # Pas de ordering défini : les pages s'affichent dans l'ordre de leur création en base de données

    # Méthode spéciale Python définissant la représentation textuelle d'un objet PageInstitutionnelle
    # Utilisée dans l'interface admin, les logs et partout où l'objet est converti en chaîne de caractères
    def __str__(self):
        """
        Représentation textuelle de l'objet.
        Utilise 'get_code_page_display()' pour afficher le nom lisible plutôt que le code brut.
        """
        # get_code_page_display() : méthode auto-générée par Django pour tout champ avec choices=
        # Traduit le code technique stocké en base en son label lisible défini dans CODE_PAGES
        # Exemple : 'HISTORIQUE' → 'Historique' | 'EQUIPE' → 'Équipe Dirigeante'
        # Sans cette méthode, __str__ retournerait le code brut 'HISTORIQUE' au lieu de 'Historique'
        return self.get_code_page_display()