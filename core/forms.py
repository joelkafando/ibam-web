# Dans core/forms.py
from django import forms

# ==========================================
# FORMULAIRE : CONTACT STANDARD
# ==========================================
class ContactForm(forms.Form):
    """
    Formulaire de contact standard basé sur forms.Form (non lié à un modèle).
    Intègre des classes CSS et des textes d'aide personnalisés pour chaque champ.
    """
    
    # Champ pour l'identité de l'expéditeur
    nom_complet = forms.CharField(
        max_length=100, 
        label="Nom complet",
        # Personnalisation de la balise HTML <input> avec style Bootstrap et texte d'exemple
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Amadou OUÉDRAOGO'})
    )
    
    # Champ pour l'adresse de réponse (vérifie automatiquement le format '@')
    email = forms.EmailField(
        label="Adresse Email",
        # Balise <input type="email"> avec attributs visuels
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ex: amadou@email.com'})
    )
    
    # Champ pour l'objet du courrier électronique
    sujet = forms.CharField(
        max_length=150, 
        label="Sujet du message",
        # Limite la saisie à 150 caractères pour éviter des titres trop longs
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Demande d\'information'})
    )
    
    # Zone de texte libre pour le corps du message
    message = forms.CharField(
        label="Votre Message",
        # Utilisation d'une balise <textarea> configurée sur 5 lignes de hauteur
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Écrivez votre message ici...'})
    )
