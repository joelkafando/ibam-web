from django import forms
from academics.models import RessourcePedagogique, DisponibiliteEnseignant, Filiere

# ==========================================
# 1. FORMULAIRE : DÉPÔT DE SUPPORT DE COURS
# ==========================================
class DepotCoursForm(forms.ModelForm):
    class Meta:
        model = RessourcePedagogique
        # L'enseignant est exclu car il est automatiquement injecté depuis request.user dans la vue
        fields = ['filiere', 'niveau_etude', 'titre_cours', 'fichier']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Injection dynamique des styles Bootstrap
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        
        # Personnalisation des placeholders et labels
        self.fields['filiere'].empty_label = "--- Sélectionner la filière cible ---"
        self.fields['niveau_etude'].widget.attrs.update({'class': 'form-control custom-select'})
        self.fields['titre_cours'].widget.attrs.update({'placeholder': 'Ex: Algorithmique avancée - Chapitre 1'})
        self.fields['fichier'].widget.attrs.update({'class': 'form-control-file'})  # Style spécifique pour les fichiers


# ==========================================
# 2. FORMULAIRE : SOUCOUMISSION DES DISPONIBILITÉS
# ==========================================
class DisponibiliteForm(forms.ModelForm):
    class Meta:
        model = DisponibiliteEnseignant
        # L'enseignant est exclu car géré automatiquement en backend
        fields = ['jour', 'periode', 'note_complementaire']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Injection des classes Bootstrap pour un design harmonisé
        self.fields['jour'].widget.attrs.update({'class': 'form-control custom-select'})
        self.fields['periode'].widget.attrs.update({'class': 'form-control custom-select'})
        
        # Le champ textuel bénéficie d'une zone de texte adaptée
        self.fields['note_complementaire'].widget = forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Ex: Uniquement disponible à partir de 10h le matin ou indisponible le mercredi après-midi.'
        })
