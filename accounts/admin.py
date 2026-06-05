from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur

@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    # Affichage des colonnes dans la liste d'administration
    list_display = ('username', 'email', 'role_user', 'filiere', 'is_staff')
    
    # Filtres de recherche latéraux
    list_filter = ('role_user', 'filiere', 'is_staff', 'is_superuser')
    
    # Ajout des champs personnalisés IBAM au formulaire d'édition standard de Django
    fieldsets = UserAdmin.fieldsets + (
        ('Informations Institutionnelles IBAM', {'fields': ('role_user', 'filiere')}),
    )
    
    # Ajout des champs personnalisés lors du formulaire de création rapide d'un compte
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations Institutionnelles IBAM', {'fields': ('role_user', 'filiere')}),
    )
