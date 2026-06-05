from django.db import models

# ==========================================
# MODÈLE : PAGE INSTITUTIONNELLE
# ==========================================
class PageInstitutionnelle(models.Model):
    """
    Modèle gérant le contenu éditorial des pages de présentation de l'établissement.
    Fonctionne comme un mini-CMS basé sur un code de page unique pour lier le contenu aux templates.
    """
    
    # Identifiants fixes uniques servant de repères pour l'affichage (Code technique, Libellé admin)
    CODE_PAGES = [
        ('PRESENTATION', 'Présentation & Missions'),
        ('HISTORIQUE', 'Historique'),
        ('EQUIPE', 'Équipe Dirigeante'),
    ]
    
    # Code d'identification unique obligatoire pour lier de manière stable chaque ligne à sa route/vue
    code_page = models.CharField(
        max_length=20, 
        choices=CODE_PAGES, 
        unique=True, 
        verbose_name="Page cible"
    )
    
    # Titre de niveau 1 (H1) qui s'affichera en haut de la page concernée
    titre_principal = models.CharField(max_length=200, verbose_name="Grand Titre de la Page")
    
    # Phrase d'accroche ou texte optionnel placé juste sous le titre principal
    sous_titre = models.CharField(max_length=250, blank=True, null=True, verbose_name="Sous-titre / Accroche")
    
    # Premier paragraphe de présentation (optionnel), souvent mis en valeur graphiquement
    introduction = models.TextField(blank=True, null=True, verbose_name="Texte d'introduction")
    
    # Bloc principal contenant le cœur de l'information éditoriale de la page
    contenu_principal = models.TextField(
        verbose_name="Corps du texte / Contenu principal", 
        help_text="Vous pouvez utiliser du texte ou du HTML basique"
    )
    
    # Colonne ou encadré de texte additionnel (optionnel) destiné aux barres latérales (sidebars)
    bloc_secondaire = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Bloc d'information complémentaire"
    )
    
    # Horodatage automatique enregistrant la date et l'heure exactes de chaque modification (auto_now=True)
    derniere_mise_a_jour = models.DateTimeField(auto_now=True)

    # Paramètres de gestion et d'affichage du modèle
    class Meta:
        verbose_name = "Page Institutionnelle"           # Nom unique dans le panneau admin
        verbose_name_plural = "Pages Institutionnelles"   # Nom au pluriel dans le panneau admin

    def __str__(self):
        """
        Représentation textuelle de l'objet.
        Utilise 'get_code_page_display()' pour afficher le nom lisible (ex: Historique) plutôt que le code brut.
        """
        return self.get_code_page_display()
