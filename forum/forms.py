# Importation du module forms de Django pour créer des formulaires liés aux modèles
from django import forms

# Importation des modèles du forum sur lesquels les formulaires sont basés
from .models import SujetForum, ReponseForum


# ==========================================
# FORMULAIRE : CRÉATION D'UN NOUVEAU SUJET
# ==========================================

# Formulaire basé sur le modèle SujetForum (ModelForm génère les champs automatiquement)
class SujetForumForm(forms.ModelForm):

    # Classe interne Meta : configure le lien entre le formulaire et le modèle Django
    class Meta:

        # Modèle Django associé à ce formulaire
        model = SujetForum

        # Champs exposés dans le formulaire
        # "auteur", "date_creation" et "est_epinglé" sont volontairement exclus :
        # - auteur : injecté depuis request.user dans la vue (commit=False)
        # - date_creation : renseigné automatiquement par auto_now_add=True
        # - est_epinglé : réservé à l'administration, non modifiable par l'utilisateur
        fields = ['categorie', 'titre', 'message_origine']

        # Dictionnaire de widgets : personnalise le rendu HTML de chaque champ
        widgets = {

            # Champ "categorie" : menu déroulant avec style Bootstrap arrondi
            # "rounded-pill" applique des bords très arrondis (style badge Bootstrap)
            'categorie': forms.Select(attrs={
                'class': 'form-control rounded-pill'
            }),

            # Champ "titre" : champ texte simple avec style Bootstrap et texte indicatif
            # "placeholder" : texte grisé affiché dans le champ vide pour guider l'utilisateur
            'titre': forms.TextInput(attrs={
                'class': 'form-control rounded-pill',
                'placeholder': 'Ex: Recherche de stage en Licence 3'
            }),

            # Champ "message_origine" : zone de texte multi-lignes pour le message d'ouverture
            # "rows=6" : hauteur du textarea fixée à 6 lignes visibles
            # "placeholder" : invite l'utilisateur à décrire son problème ou partager une info
            'message_origine': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Expliquez votre problème ou partagez votre information ici...'
            }),
        }


# ==========================================
# FORMULAIRE : AJOUT D'UNE RÉPONSE
# ==========================================

# Formulaire basé sur le modèle ReponseForum (ModelForm génère le champ automatiquement)
class ReponseForumForm(forms.ModelForm):

    # Classe interne Meta : configure le lien entre le formulaire et le modèle Django
    class Meta:

        # Modèle Django associé à ce formulaire
        model = ReponseForum

        # Seul le champ "contenu" est exposé dans le formulaire
        # "sujet" et "auteur" sont exclus car injectés dans la vue via commit=False
        # "date_publication" est exclu car renseigné automatiquement par auto_now_add=True
        fields = ['contenu']

        # Dictionnaire de widgets : personnalise le rendu HTML du champ
        widgets = {

            # Champ "contenu" : zone de texte compacte pour saisir une réponse courte
            # "rows=3" : textarea plus petit que celui du sujet (réponse = message plus court)
            # "placeholder" : guide l'utilisateur sur ce qu'il peut écrire
            'contenu': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Écrivez votre réponse ou commentaire...'
            }),
        }