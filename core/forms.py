# Importation du module forms de Django pour créer des formulaires HTML
# forms.Form : classe de base pour les formulaires non liés à un modèle de base de données
# forms.ModelForm : alternative liée à un modèle (non utilisée ici)
from django import forms


# ==========================================
# FORMULAIRE : CONTACT STANDARD
# ==========================================

# Définition du formulaire de contact qui hérite de forms.Form
# forms.Form : formulaire autonome sans liaison directe à un modèle Django
# Contrairement à ModelForm, les données ne sont pas automatiquement sauvegardées en base de données
# La vue qui utilise ce formulaire devra gérer manuellement l'envoi de l'email ou la sauvegarde
class ContactForm(forms.Form):
    """
    Formulaire de contact standard basé sur forms.Form (non lié à un modèle).
    Intègre des classes CSS et des textes d'aide personnalisés pour chaque champ.
    """

    # Champ texte pour recueillir le nom complet de l'expéditeur du message
    # max_length=100 : limite la saisie à 100 caractères, validée côté serveur par Django
    # label : texte affiché devant le champ dans le formulaire HTML rendu (remplace le nom de variable)
    nom_complet = forms.CharField(
        max_length=100,             # Longueur maximale autorisée : génère une erreur si dépassée
        label="Nom complet",        # Label affiché dans le template via {{ form.nom_complet.label }}

        # widget : définit la balise HTML générée pour ce champ et ses attributs visuels
        # forms.TextInput : génère une balise <input type="text"> dans le HTML final
        # attrs : dictionnaire d'attributs HTML injectés directement dans la balise <input>
        widget=forms.TextInput(attrs={
            'class': 'form-control',                # Classe CSS Bootstrap pour styliser le champ
            'placeholder': 'Ex: Amadou OUÉDRAOGO'  # Texte grisé affiché à l'intérieur du champ vide
        })
    )

    # Champ email avec validation automatique du format par Django
    # EmailField : vérifie la présence d'un '@' et d'un domaine valide avant acceptation
    # Si le format est invalide, Django affiche automatiquement un message d'erreur localisé
    email = forms.EmailField(
        label="Adresse Email",      # Label affiché dans le template via {{ form.email.label }}

        # forms.EmailInput : génère une balise <input type="email"> dans le HTML
        # type="email" active aussi la validation native du navigateur (mobile : clavier adapté)
        widget=forms.EmailInput(attrs={
            'class': 'form-control',                    # Classe CSS Bootstrap standard
            'placeholder': 'Ex: amadou@email.com'      # Exemple de format attendu affiché dans le champ vide
        })
    )

    # Champ texte pour l'objet ou le titre du message envoyé
    # max_length=150 : limite à 150 caractères pour éviter des sujets excessivement longs
    # required=True par défaut : le champ est obligatoire si non précisé (comportement Django standard)
    sujet = forms.CharField(
        max_length=150,                 # Limite stricte de 150 caractères vérifiée côté serveur
        label="Sujet du message",       # Label affiché dans le template HTML

        # forms.TextInput : génère un <input type="text"> pour la saisie d'une ligne de texte
        widget=forms.TextInput(attrs={
            'class': 'form-control',                        # Classe CSS Bootstrap pour l'apparence
            'placeholder': 'Ex: Demande d\'information'    # Exemple indicatif affiché dans le champ
            #                                ^ Apostrophe échappée avec \ pour éviter une erreur de syntaxe Python
        })
    )

    # Champ texte multiligne pour le corps complet du message de l'expéditeur
    # CharField est utilisé ici avec un widget Textarea pour obtenir une zone de texte multiligne
    # Pas de max_length défini : aucune limite de longueur imposée sur ce champ
    message = forms.CharField(
        label="Votre Message",      # Label affiché dans le template HTML

        # forms.Textarea : génère une balise <textarea></textarea> au lieu d'un <input>
        # Permet la saisie de texte sur plusieurs lignes (corps du message)
        widget=forms.Textarea(attrs={
            'class': 'form-control',                        # Classe CSS Bootstrap standard
            'rows': 5,                                      # Hauteur initiale de la zone de texte (5 lignes visibles)
            #        ^ Attribut HTML natif : rows="5" dans la balise <textarea>
            'placeholder': 'Écrivez votre message ici...'  # Texte indicatif affiché dans la zone vide
        })
    )