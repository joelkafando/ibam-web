# Importation du module admin de Django pour accéder à l'interface d'administration
from django.contrib import admin

# Importation du modèle PageInstitutionnelle depuis le fichier models.py de l'application courante
# Ce modèle contient les champs et la logique des pages statiques de l'établissement
from .models import PageInstitutionnelle


# ==========================================
# CONFIGURATION DE L'ADMINISTRATION DES PAGES INSTITUTIONNELLES
# ==========================================

# Décorateur Django qui enregistre le modèle PageInstitutionnelle dans l'interface d'administration
# et l'associe à la classe PageInstitutionnelleAdmin qui définit son comportement visuel
@admin.register(PageInstitutionnelle)
class PageInstitutionnelleAdmin(admin.ModelAdmin):

    # Définition des colonnes affichées dans le tableau récapitulatif de la liste des pages
    # Chaque chaîne correspond à un champ du modèle ou une méthode de la classe d'administration
    list_display = (
        'code_page',              # Identifiant technique unique de la page (ex: 'about', 'contact')
        'titre_principal',        # Titre principal affiché en haut de la page institutionnelle
        'derniere_mise_a_jour'    # Date et heure de la dernière modification enregistrée
    )

    # Organisation du formulaire de création et de modification en sections thématiques nommées
    # Chaque tuple représente une section : ('Nom de la section', {'fields': (...)})
    fieldsets = (

        # SECTION 1 : Paramètres d'identification et de configuration structurelle de la page
        # Regroupe les champs techniques qui définissent l'identité de la page
        ("Configuration de la Page", {
            'fields': ('code_page', 'titre_principal', 'sous_titre')
            #           ^ ID unique   ^ Titre H1          ^ Sous-titre affiché sous le titre principal
        }),

        # SECTION 2 : Champs éditoriaux contenant le texte principal de la page
        # Regroupe les zones de saisie du contenu rédigé par l'administrateur
        ("Contenu Editorial", {
            'fields': ('introduction', 'contenu_principal')
            #           ^ Texte d'accroche  ^ Corps principal de l'article ou de la page
        }),

        # SECTION 3 : Éléments optionnels affichés dans la colonne latérale de la page
        # 'description' : texte d'aide affiché sous le titre de la section dans le formulaire admin
        ("Blocs Complémentaires", {
            'fields': ('bloc_secondaire',),     # Virgule obligatoire : force Python à reconnaître un tuple à un seul élément
            'description': "Informations affichées dans la colonne latérale droite de la page."
            #               ^ Indice contextuel visible sous le titre de la section dans l'admin
        }),
    )

    # Surcharge de la méthode get_readonly_fields() pour adapter dynamiquement les champs verrouillés
    # selon que l'on crée une nouvelle page (INSERT) ou que l'on modifie une page existante (UPDATE)
    def get_readonly_fields(self, request, obj=None):
        """
        Surcharge dynamique des champs en lecture seule (Read-Only).
        Verrouille le champ 'code_page' lors d'une modification pour préserver
        les liaisons matérielles avec vos templates ou vos vues Django.
        """
        # Paramètre 'request' : objet de la requête HTTP en cours (non utilisé ici mais requis par la signature)
        # Paramètre 'obj' : objet du modèle en cours d'édition, ou None si création d'un nouvel enregistrement

        # Vérification du contexte : si obj n'est pas None, on est en mode MODIFICATION d'une page existante
        # obj contient l'instance complète du modèle PageInstitutionnelle en cours d'édition
        if obj:
            # En mode UPDATE : on verrouille 'code_page' en lecture seule pour empêcher sa modification
            # Raison : le code_page est utilisé comme identifiant dans les vues et templates Django
            # Le modifier casserait tous les liens qui y font référence (reverse(), {% url %}, etc.)
            # self.readonly_fields : tuple des champs déjà déclarés en lecture seule dans la classe
            # + ('code_page',) : ajout dynamique du champ 'code_page' à la liste existante
            return self.readonly_fields + ('code_page',)
            #      ^ Champs déjà verrouillés   ^ 'code_page' verrouillé uniquement en mode modification

        # En mode INSERT (obj est None) : 'code_page' reste éditable pour saisir l'identifiant unique
        # Un administrateur doit pouvoir définir librement le code lors de la création de la page
        return self.readonly_fields
        #      ^ Retourne uniquement les champs de base verrouillés, sans ajouter 'code_page'