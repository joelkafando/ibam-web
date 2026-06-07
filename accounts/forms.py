# Importation du module forms de Django pour créer et configurer des formulaires HTML
from django import forms

# Importation de la fonction retournant dynamiquement le modèle User actif du projet
# Respecte le paramètre AUTH_USER_MODEL défini dans settings.py
from django.contrib.auth import get_user_model

# Importation du formulaire de création d'utilisateur natif de Django
# Fournit les champs username, password1 et password2 avec toute la validation associée
from django.contrib.auth.forms import UserCreationForm

# Importation du modèle Filiere depuis l'application academics
# Permet de lier chaque inscription d'étudiant à une formation existante en base de données
from academics.models import Filiere


# Appel de la fonction pour récupérer le modèle User personnalisé du projet (accounts.Utilisateur)
# Stocké dans la variable User pour être réutilisé dans les deux formulaires ci-dessous
User = get_user_model()


# ==========================================
# 1. FORMULAIRE : INSCRIPTION DES ÉTUDIANTS
# ==========================================

# Définition du formulaire d'inscription étudiant
# Hérite de UserCreationForm pour bénéficier des champs et validations natifs de Django
# (username, password1, password2 avec vérification de correspondance et de robustesse)
class EtudiantRegisterForm(UserCreationForm):
    """
    Formulaire d'inscription personnalisé étendant le formulaire de création de base de Django.
    Ajoute des champs obligatoires et lie l'étudiant à une filière et un niveau d'études.
    """

    # Champ texte pour le prénom : rendu obligatoire (required=True) et avec un label francisé
    # Surcharge le champ hérité d'AbstractUser qui n'est pas obligatoire par défaut
    first_name = forms.CharField(label="Prénom", required=True)

    # Champ texte pour le nom de famille : même logique que first_name
    last_name = forms.CharField(label="Nom", required=True)

    # Champ email avec validation automatique du format (présence du @, domaine, etc.)
    # required=True : l'inscription échoue si ce champ est laissé vide
    email = forms.EmailField(label="Adresse Email", required=True)

    # Champ de sélection dynamique lié à la table Filiere en base de données
    # ModelChoiceField : génère un <select> HTML dont les options sont des objets Django
    filiere = forms.ModelChoiceField(
        queryset=Filiere.objects.all(),                     # Requête SQL qui récupère toutes les filières existantes
        label="Votre Filière",                              # Label affiché devant le menu déroulant dans le formulaire
        required=True,                                      # Champ obligatoire : une filière doit être sélectionnée
        empty_label="-- Sélectionnez votre filière --"      # Option vide affichée par défaut en haut de la liste
    )

    # Liste de tuples définissant les options fixes du niveau d'études
    # Format : ('valeur_envoyée_en_POST', 'Label affiché dans le <select>')
    CHOICES_NIVEAU = [
        ('Licence 1', 'Licence 1'),     # Première année de Licence
        ('Licence 2', 'Licence 2'),     # Deuxième année de Licence
        ('Licence 3', 'Licence 3'),     # Troisième année de Licence
        ('Master 1', 'Master 1'),       # Première année de Master
        ('Master 2', 'Master 2'),       # Deuxième année de Master
    ]

    # Champ de sélection statique basé sur la liste CHOICES_NIVEAU ci-dessus
    # ChoiceField (sans Model) : les options sont fixes et non issues de la base de données
    niveau_etude = forms.ChoiceField(
        choices=CHOICES_NIVEAU,             # Liste des options disponibles dans le menu déroulant
        label="Votre Niveau d'études",      # Label affiché devant le champ dans le formulaire HTML
        required=True                       # Sélection obligatoire : le formulaire ne peut pas être soumis sans valeur
    )

    # Classe interne Meta : configure les métadonnées du formulaire (modèle cible et champs inclus)
    # Hérite de UserCreationForm.Meta pour ne pas perdre ses configurations natives
    class Meta(UserCreationForm.Meta):

        # Modèle Django ciblé par ce formulaire : les données seront sauvegardées dans la table Utilisateur
        model = User

        # Fusion des champs natifs de UserCreationForm (username, password1, password2)
        # avec les nouveaux champs personnalisés ajoutés dans cette classe
        # L'opérateur + concatène les deux tuples sans écraser les champs natifs
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'filiere', 'niveau_etude')
        #        ^ Champs natifs hérités (username, password1, password2)    ^ Champs personnalisés ajoutés

    # Surcharge de la méthode save() pour personnaliser la sauvegarde de l'utilisateur
    def save(self, commit=True):
        """
        Surcharge de la méthode de sauvegarde pour injecter des valeurs par défaut
        et lier les données nettoyées (cleaned_data) au profil de l'utilisateur.
        """
        # Appel de la méthode save() parente avec commit=False
        # commit=False : crée l'objet Utilisateur en mémoire SANS l'écrire en base de données
        # Indispensable pour pouvoir modifier l'objet avant sa sauvegarde définitive
        user = super().save(commit=False)

        # Attribution automatique du rôle 'ETUDIANT' à tout utilisateur s'inscrivant via ce formulaire
        # Empêche un étudiant de se créer un compte avec un rôle ENSEIGNANT ou ADMIN
        user.role_user = 'ETUDIANT'

        # Liaison de l'objet Filiere sélectionné dans le formulaire à l'instance utilisateur
        # cleaned_data : dictionnaire des données validées et nettoyées par Django après soumission du formulaire
        user.filiere = self.cleaned_data['filiere']

        # Vérification préventive : hasattr() contrôle si le champ 'niveau_etude' existe sur le modèle
        # Protège contre une AttributeError si le champ n'est pas défini dans le modèle Utilisateur
        if hasattr(user, 'niveau_etude'):
            # Attribution du niveau d'études choisi dans le formulaire à l'instance utilisateur
            user.niveau_etude = self.cleaned_data['niveau_etude']

        # Sauvegarde définitive en base de données uniquement si commit=True (comportement par défaut)
        # commit=False peut être utilisé par des vues qui ont besoin de modifier l'objet avant la sauvegarde
        if commit:
            user.save()     # Génère un INSERT SQL dans la table de la base de données

        # Retourne l'instance utilisateur (sauvegardée ou non selon commit) pour utilisation dans la vue
        return user


# ==========================================
# 2. FORMULAIRE : MODIFICATION DU PROFIL
# ==========================================

# Formulaire de mise à jour du profil étudiant
# Hérite de forms.ModelForm : génère automatiquement les champs à partir du modèle User
class ModifierProfilEtudiantForm(forms.ModelForm):
    """
    Permet à l'étudiant connecté de modifier ses informations de base de manière sécurisée.
    Verrouille volontairement l'accès aux champs académiques (filière, niveau) pour éviter les fraudes.
    """

    # Classe Meta : configure le modèle source et les champs exposés dans le formulaire
    class Meta:

        # Modèle Django ciblé : les modifications seront sauvegardées dans la table Utilisateur
        model = User

        # Liste blanche stricte des champs modifiables par l'étudiant
        # filiere et niveau_etude sont volontairement absents pour empêcher toute modification frauduleuse
        fields = ['first_name', 'last_name', 'email']

        # Dictionnaire de surcharge des labels affichés devant chaque champ dans le template HTML
        labels = {
            'first_name': 'Prénom',         # Remplace le label par défaut 'First name' par 'Prénom'
            'last_name': 'Nom de famille',  # Remplace 'Last name' par 'Nom de famille'
            'email': 'Adresse E-mail',      # Remplace 'Email address' par 'Adresse E-mail'
        }

        # Dictionnaire de personnalisation des widgets HTML associés à chaque champ
        # Un widget définit comment le champ est rendu visuellement en HTML
        widgets = {
            # TextInput : génère un <input type="text"> avec les classes CSS Bootstrap injectées
            # 'form-control' : applique le style Bootstrap standard aux champs de saisie
            # 'rounded-pill' : arrondit les bords du champ pour un rendu visuel moderne
            'first_name': forms.TextInput(attrs={'class': 'form-control rounded-pill'}),

            # Même widget et mêmes classes CSS pour le champ nom de famille
            'last_name': forms.TextInput(attrs={'class': 'form-control rounded-pill'}),

            # EmailInput : génère un <input type="email"> avec validation navigateur du format email
            # Les classes CSS Bootstrap sont identiques pour assurer une cohérence visuelle
            'email': forms.EmailInput(attrs={'class': 'form-control rounded-pill'}),
        }