from django.shortcuts import render
from django.contrib import messages  # IMPORTATION INDISPENSABLE : Nécessaire pour faire fonctionner messages.success
from announcements.models import Announcement
from academics.models import Filiere
from .forms import ContactForm

# ==========================================
# VUE : PAGE D'ACCUEIL PRINCIPALE
# ==========================================
def home(request):
    """
    Gère l'affichage de la page d'accueil.
    Extrait dynamiquement les 3 publications les plus récentes et actives.
    """
    # Requête de sélection : filtre les annonces actives et limite le résultat aux 3 premières (slicing [:3])
    latest_announcements = Announcement.objects.filter(is_active=True)[:3]

    # Rendu graphique avec injection des données récupérées
    return render(request, 'core/home.html', {
        'announcements': latest_announcements
    })


# ==========================================
# VUES ÉDITORIALES COMPLÉMENTAIRES
# ==========================================
def about(request):
    """Affiche la page de présentation générale du site."""
    return render(request, 'core/about.html')


def admissions(request):
    """Affiche les informations relatives aux conditions d'admission."""
    return render(request, 'core/admissions.html')


# ==========================================
# VUE : TRAITEMENT DU FORMULAIRE DE CONTACT
# ==========================================
def contact(request):
    """
    Gère l'affichage de la page contact (GET) et la réception 
    du formulaire de message envoyé à l'administration (POST).
    """
    # Cas 1 : Soumission des données par l'utilisateur (Méthode POST)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        
        # Vérification des règles de validation définies dans core/forms.py
        if form.is_valid():
            # Extraction des données nettoyées et sécurisées par Django
            nom = form.cleaned_data['nom_complet']
            
            # Enregistrement du message de notification à destination du template HTML
            messages.success(request, f"Merci {nom}, votre message a bien été envoyé à l'administration de l'IBAM !")
            
            # Instanciation d'un nouveau formulaire vierge pour vider les champs à l'écran
            form = ContactForm() 
            
    # Cas 2 : Premier accès à la page par le visiteur (Méthode GET)
    else:
        form = ContactForm()
        
    # Rendu final du formulaire de contact, vide ou accompagné de ses erreurs/messages de succès
    return render(request, 'core/contact.html', {'form': form})


# ==========================================
# VUE : CATALOGUE DES FORMATIONS
# ==========================================
def formations(request):
    """Récupère l'intégralité du catalogue des filières d'études pour affichage public."""
    # Requête globale sur la table Filiere
    filieres = Filiere.objects.all()
    return render(request, 'core/formations.html', {'filieres': filieres})


# ==========================================
# VUES DÉDIÉES AUX PAGES INSTITUTIONNELLES DE L'IBAM
# ==========================================
def presentation(request):
    """Redirige et affiche le contenu éditorial des missions (réutilise le template about.html)."""
    return render(request, 'core/about.html')


def historique(request):
    """Affiche l'historique de la fondation de l'établissement."""
    return render(request, 'core/historique.html')


def equipe(request):
    """Affiche l'organigramme et les membres du corps enseignant et administratif dirigeant."""
    return render(request, 'core/equipe.html')
