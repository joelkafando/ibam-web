from django.contrib import admin
from .models import CategorieForum, SujetForum, ReponseForum

@admin.register(CategorieForum)
class CategorieForumAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description')

@admin.register(SujetForum)
class SujetForumAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'auteur', 'date_creation', 'est_epinglé')
    list_filter = ('categorie', 'est_epinglé')
    search_fields = ('titre', 'message_origine')

@admin.register(ReponseForum)
class ReponseForumAdmin(admin.ModelAdmin):
    list_display = ('auteur', 'sujet', 'date_publication')
    search_fields = ('contenu',)
