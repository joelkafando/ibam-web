from django import forms
from .models import SujetForum, ReponseForum

# ==========================================
# FORMULAIRE : CRÉATION D'UN NOUVEAU SUJET
# ==========================================
class SujetForumForm(forms.ModelForm):
    class Meta:
        model = SujetForum
        # L'auteur, la date et le statut épinglé sont gérés automatiquement en arrière-plan
        fields = ['categorie', 'titre', 'message_origine']
        
        widgets = {
            'categorie': forms.Select(attrs={'class': 'form-control rounded-pill'}),
            'titre': forms.TextInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Ex: Recherche de stage en Licence 3'}),
            'message_origine': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Expliquez votre problème ou partagez votre information ici...'}),
        }


# ==========================================
# FORMULAIRE : AJOUT D'UNE RÉPONSE
# ==========================================
class ReponseForumForm(forms.ModelForm):
    class Meta:
        model = ReponseForum
        fields = ['contenu']
        
        widgets = {
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Écrivez votre réponse ou commentaire...'}),
        }
