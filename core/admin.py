from django.contrib import admin
from .models import PageInstitutionnelle  # Importation du modèle associé

# ==========================================
# CONFIGURATION DE L'ADMINISTRATION DES PAGES INSTITUTIONNELLES
# ==========================================

# Décorateur officiel pour lier le modèle PageInstitutionnelle à sa classe d'administration
@admin.register(PageInstitutionnelle)
class PageInstitutionnelleAdmin(admin.ModelAdmin):
    # Colonnes visibles dans le tableau récapitulatif des pages institutionnelles
    list_display = ('code_page', 'titre_principal', 'derniere_mise_a_jour')
    
    # Organisation visuelle du formulaire de saisie structurée en sections thématiques
    fieldsets = (
        # Section 1 : Paramètres structurels et identité de la page
        ("Configuration de la Page", {
            'fields': ('code_page', 'titre_principal', 'sous_titre')
        }),
        # Section 2 : Corps du texte et données textuelles de l'article
        ("Contenu Editorial", {
            'fields': ('introduction', 'contenu_principal')
        }),
        # Section 3 : Éléments facultatifs ou widgets périphériques
        ("Blocs Complémentaires", {
            'fields': ('bloc_secondaire',),
            'description': "Informations affichées dans la colonne latérale droite de la page."
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        """
        Surcharge dynamique des champs en lecture seule (Read-Only).
        Verrouille le champ 'code_page' lors d'une modification pour préserver 
        les liaisons matérielles avec vos templates ou vos vues Django.
        """
        # Si 'obj' n'est pas None, cela signifie que nous éditons une page existante (Mode UPDATE)
        if obj:
            # On retourne la liste existante enrichie du champ technique 'code_page'
            return self.readonly_fields + ('code_page',)
        
        # Si 'obj' est None, nous sommes sur un nouveau formulaire (Mode INSERT), le champ reste saisissable
        return self.readonly_fields
