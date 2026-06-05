from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from academics.models import Filiere  # Importation du modèle Filiere pour lier les inscriptions aux formations

# Récupération dynamique du modèle Utilisateur actif du projet (User personnalisé ou par défaut)
User = get_user_model()

# ==========================================
# 1. FORMULAIRE : INSCRIPTION DES ÉTUDIANTS
# ==========================================
class EtudiantRegisterForm(UserCreationForm):
    """
    Formulaire d'inscription personnalisé étendant le formulaire de création de base de Django.
    Ajoute des champs obligatoires et lie l'étudiant à une filière et un niveau d'études.
    """
    # Surcharge des champs de base pour les rendre obligatoires lors de la soumission
    first_name = forms.CharField(label="Prénom", required=True)
    last_name = forms.CharField(label="Nom", required=True)
    email = forms.EmailField(label="Adresse Email", required=True)
    
    # Menu déroulant dynamique alimenté par toutes les lignes existantes de la table Filiere
    filiere = forms.ModelChoiceField(
        queryset=Filiere.objects.all(),
        label="Votre Filière",
        required=True,
        empty_label="-- Sélectionnez votre filière --"  # Libellé par défaut affiché dans la liste
    )
    
    # Liste fixe des options de parcours académique disponibles
    CHOICES_NIVEAU = [
        ('Licence 1', 'Licence 1'),
        ('Licence 2', 'Licence 2'),
        ('Licence 3', 'Licence 3'),
        ('Master 1', 'Master 1'),
        ('Master 2', 'Master 2'),
    ]
    
    # Menu déroulant statique basé sur la liste CHOICES_NIVEAU
    niveau_etude = forms.ChoiceField(
        choices=CHOICES_NIVEAU,
        label="Votre Niveau d'études",
        required=True
    )

    # Configuration des métadonnées du formulaire d'inscription
    class Meta(UserCreationForm.Meta):
        model = User
        # Fusion des champs par défaut (username, password) avec nos nouveaux champs personnalisés
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'filiere', 'niveau_etude')

    def save(self, commit=True):
        """
        Surcharge de la méthode de sauvegarde pour injecter des valeurs par défaut 
        et lier les données nettoyées (cleaned_data) au profil de l'utilisateur.
        """
        # Génération de l'instance utilisateur en mémoire sans l'écrire immédiatement en base (commit=False)
        user = super().save(commit=False)
        
        # Attribution automatique du rôle pour sécuriser les permissions de l'espace étudiant
        user.role_user = 'ETUDIANT'  
        
        # Liaison de l'objet Filiere sélectionné à l'utilisateur
        user.filiere = self.cleaned_data['filiere']
        
        # Vérification de sécurité : applique le niveau d'étude si le champ existe sur votre modèle Utilisateur
        if hasattr(user, 'niveau_etude'):
            user.niveau_etude = self.cleaned_data['niveau_etude']
            
        # Écriture définitive des données en base de données si l'argument commit est vrai
        if commit:
            user.save()
            
        return user


# ==========================================
# 2. FORMULAIRE : MODIFICATION DU PROFIL
# ==========================================
class ModifierProfilEtudiantForm(forms.ModelForm):
    """
    Permet à l'étudiant connecté de modifier ses informations de base de manière sécurisée.
    Verrouille volontairement l'accès aux champs académiques (filière, niveau) pour éviter les fraudes.
    """
    class Meta:
        model = User
        # Définition stricte des seuls champs modifiables par l'utilisateur final
        fields = ['first_name', 'last_name', 'email']
        
        # Surcharge des labels affichés à l'écran devant chaque case
        labels = {
            'first_name': 'Prénom',
            'last_name': 'Nom de famille',
            'email': 'Adresse E-mail',
        }
        
        # Personnalisation de l'affichage HTML (injection de classes CSS Bootstrap)
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control rounded-pill'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control rounded-pill'}),
            'email': forms.EmailInput(attrs={'class': 'form-control rounded-pill'}),
        }
