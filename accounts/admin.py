from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur

# Configuration visuelle du modèle Utilisateur dans le Back-Office
class UtilisateurAdmin(UserAdmin):
    # 1. Colonnes visibles dans la liste globale des utilisateurs
    list_display = ('username', 'email', 'last_name', 'first_name', 'role_user', 'filiere', 'niveau_etude', 'is_staff')
    
    # 2. Filtres latéraux pour trier rapidement les comptes
    list_filter = ('role_user', 'filiere', 'niveau_etude', 'is_staff', 'is_superuser')

    # 3. Injection des champs personnalisés dans le formulaire de modification de l'admin
    fieldsets = UserAdmin.fieldsets + (
        ('Informations Institutionnelles IBAM', {
            'fields': ('role_user', 'filiere', 'niveau_etude'),
        }),
    )

    # Configuration pour le formulaire de création de compte direct dans l'admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations Institutionnelles IBAM', {
            'fields': ('role_user', 'filiere', 'niveau_etude'),
        }),
    )

# UNIQUE ENREGISTREMENT EN BASE (Assurez-vous qu'il n'y en a pas d'autre au-dessus ou en dessous)
admin.site.register(Utilisateur, UtilisateurAdmin)
