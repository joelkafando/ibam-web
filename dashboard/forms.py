# Importation du module forms de Django pour créer des formulaires
from django import forms

# Importation des modèles nécessaires depuis l'application "academics"
from academics.models import RessourcePedagogique, DisponibiliteEnseignant, Filiere


# ==========================================
# 1. FORMULAIRE : DÉPÔT DE SUPPORT DE COURS
# ==========================================

# Définition du formulaire basé sur le modèle RessourcePedagogique
class DepotCoursForm(forms.ModelForm):

    # Classe interne Meta : configure le lien entre le formulaire et le modèle Django
    class Meta:
        # Modèle Django associé à ce formulaire
        model = RessourcePedagogique

        # Liste des champs à afficher dans le formulaire
        # "enseignant" est volontairement exclu : il est injecté automatiquement
        # depuis request.user dans la vue (l'utilisateur connecté)
        fields = ['filiere', 'niveau_etude', 'titre_cours', 'fichier']

    # Méthode d'initialisation du formulaire, appelée à chaque instanciation
    def __init__(self, *args, **kwargs):
        # Appel du constructeur parent pour initialiser correctement le formulaire
        super().__init__(*args, **kwargs)

        # Boucle sur tous les champs du formulaire pour appliquer des styles Bootstrap
        for field_name, field in self.fields.items():
            # Ajout de la classe CSS Bootstrap "form-control" à chaque champ
            field.widget.attrs.update({'class': 'form-control'})

        # Personnalisation du champ "filiere" : texte affiché quand rien n'est sélectionné
        self.fields['filiere'].empty_label = "--- Sélectionner la filière cible ---"

        # Ajout d'une classe CSS supplémentaire "custom-select" pour le champ "niveau_etude"
        # (style Bootstrap spécifique aux menus déroulants)
        self.fields['niveau_etude'].widget.attrs.update({'class': 'form-control custom-select'})

        # Ajout d'un texte indicatif (placeholder) dans le champ "titre_cours"
        self.fields['titre_cours'].widget.attrs.update({'placeholder': 'Ex: Algorithmique avancée - Chapitre 1'})

        # Remplacement de la classe CSS pour le champ fichier par "form-control-file"
        # car Bootstrap utilise une classe distincte pour les champs de type fichier
        self.fields['fichier'].widget.attrs.update({'class': 'form-control-file'})


# ==========================================
# 2. FORMULAIRE : SOUMISSION DES DISPONIBILITÉS
# ==========================================

# Définition du formulaire basé sur le modèle DisponibiliteEnseignant
class DisponibiliteForm(forms.ModelForm):

    # Classe interne Meta : configure le lien entre le formulaire et le modèle Django
    class Meta:
        # Modèle Django associé à ce formulaire
        model = DisponibiliteEnseignant

        # Champs affichés dans le formulaire
        # "enseignant" est exclu car il est géré automatiquement côté backend (via request.user)
        fields = ['jour', 'periode', 'note_complementaire']

    # Méthode d'initialisation du formulaire
    def __init__(self, *args, **kwargs):
        # Appel du constructeur parent pour initialiser le formulaire correctement
        super().__init__(*args, **kwargs)

        # Application du style Bootstrap avec "custom-select" pour le champ "jour"
        # (menu déroulant avec style Bootstrap personnalisé)
        self.fields['jour'].widget.attrs.update({'class': 'form-control custom-select'})

        # Application du même style Bootstrap "custom-select" pour le champ "periode"
        self.fields['periode'].widget.attrs.update({'class': 'form-control custom-select'})

        # Remplacement du widget par défaut du champ "note_complementaire" par un Textarea
        # pour permettre la saisie de texte sur plusieurs lignes
        self.fields['note_complementaire'].widget = forms.Textarea(attrs={
            # Classe Bootstrap pour intégrer le textarea dans le design global
            'class': 'form-control',

            # Hauteur du textarea : 3 lignes visibles
            'rows': 3,

            # Texte d'aide affiché dans le champ vide pour guider l'enseignant
            'placeholder': 'Ex: Uniquement disponible à partir de 10h le matin ou indisponible le mercredi après-midi.'
        })