# Importation de la fonction render pour compiler un template HTML avec un contexte de données
# et retourner une réponse HTTP complète au navigateur de l'utilisateur
from django.shortcuts import render

# Importation du système de messages flash de Django
# Permet d'afficher des notifications (succès, erreur, info) sur la page après une redirection ou un rendu
# INDISPENSABLE : sans cet import, messages.success() lèverait une NameError à l'exécution
from django.contrib import messages

# Importation du modèle Announcement depuis l'application announcements
# Donne accès aux publications de l'établissement pour les afficher sur la page d'accueil
from announcements.models import Announcement

# Importation du modèle Filiere depuis l'application academics
# Permet de récupérer le catalogue des formations pour la page dédiée
from academics.models import Filiere

# Importation du formulaire de contact défini dans forms.py de l'application courante
# ContactForm hérite de forms.Form (non lié à un modèle) et gère la validation des données saisies
from .forms import ContactForm


# ==========================================
# VUE : PAGE D'ACCUEIL PRINCIPALE
# ==========================================

# Vue fonction accessible sans authentification : la page d'accueil est publique
def home(request):
    """
    Gère l'affichage de la page d'accueil.
    Extrait dynamiquement les 3 publications les plus récentes et actives.
    """
    # Filtrage des annonces actives uniquement (is_active=True) puis limitation aux 3 premières
    # .filter(is_active=True) : génère un WHERE is_active = 1 en SQL
    # [:3] : slicing Python appliqué au QuerySet → équivalent SQL de LIMIT 3
    # L'ordre est défini par le Meta.ordering du modèle Announcement : ['-date_published'] (plus récentes en premier)
    latest_announcements = Announcement.objects.filter(is_active=True)[:3]

    # Rendu de la page d'accueil avec injection des 3 annonces récupérées dans le contexte
    # 'announcements' : clé accessible dans le template via {{ announcements }} ou {% for a in announcements %}
    return render(request, 'core/home.html', {
        'announcements': latest_announcements   # Les 3 annonces actives les plus récentes
    })


# ==========================================
# VUES ÉDITORIALES COMPLÉMENTAIRES
# ==========================================

# Vue simple de rendu statique : aucune donnée dynamique à injecter
def about(request):
    """Affiche la page de présentation générale du site."""
    # Rendu direct du template sans contexte : le contenu est entièrement statique dans le HTML
    return render(request, 'core/about.html')


# Vue simple de rendu statique pour les informations d'admission
def admissions(request):
    """Affiche les informations relatives aux conditions d'admission."""
    # Pas de requête base de données nécessaire : page purement informative et statique
    return render(request, 'core/admissions.html')


# ==========================================
# VUE : TRAITEMENT DU FORMULAIRE DE CONTACT
# ==========================================

# Vue gérant deux comportements distincts selon la méthode HTTP de la requête (GET ou POST)
def contact(request):
    """
    Gère l'affichage de la page contact (GET) et la réception
    du formulaire de message envoyé à l'administration (POST).
    """
    # Vérification de la méthode HTTP de la requête entrante
    # POST : l'utilisateur a rempli et soumis le formulaire de contact
    if request.method == 'POST':

        # Instanciation du formulaire avec les données soumises par l'utilisateur
        # request.POST : dictionnaire Python contenant toutes les valeurs saisies dans le formulaire HTML
        form = ContactForm(request.POST)

        # Déclenchement de toutes les validations définies dans ContactForm
        # Vérifie : champs obligatoires remplis, format email valide, longueurs max respectées...
        if form.is_valid():

            # Extraction de la valeur nettoyée et sécurisée du champ 'nom_complet'
            # cleaned_data : dictionnaire des données validées et assainies par Django (XSS protégé)
            # On récupère uniquement le nom ici pour personnaliser le message de confirmation
            nom = form.cleaned_data['nom_complet']

            # Création d'un message flash de succès stocké en session
            # Il sera affiché dans le template via {% if messages %}...{% endif %}
            # f-string : personnalise le message avec le prénom saisi par l'utilisateur
            # Note : dans un projet réel, c'est ici qu'on appellerait send_mail() pour envoyer l'email
            messages.success(request, f"Merci {nom}, votre message a bien été envoyé à l'administration de l'IBAM !")

            # Réinitialisation du formulaire avec une instance vierge après envoi réussi
            # Pattern PRG allégé : vide les champs sans rediriger, évite la re-soumission accidentelle
            # Si on ne réinitialisait pas, les données saisies resteraient affichées dans les champs
            form = ContactForm()
            #      ^ Nouvelle instance vide : tous les champs du formulaire sont réinitialisés à l'écran

    # Méthode GET : première visite de la page, affichage du formulaire vierge
    else:
        # Instanciation d'un formulaire vide sans données pré-remplies
        # Sera rendu dans le template pour que l'utilisateur puisse le remplir
        form = ContactForm()

    # Rendu final du template de contact avec transmission du formulaire
    # Trois cas possibles selon le flux :
    # 1. GET initial : formulaire vide affiché
    # 2. POST invalide : formulaire avec erreurs de validation affichées sous chaque champ
    # 3. POST valide : nouveau formulaire vide affiché + message flash de succès visible
    return render(request, 'core/contact.html', {'form': form})
    #                                             ^ 'form' accessible dans le template via {{ form }}


# ==========================================
# VUE : CATALOGUE DES FORMATIONS
# ==========================================

# Vue publique affichant la liste complète des filières d'études disponibles
def formations(request):
    """Récupère l'intégralité du catalogue des filières d'études pour affichage public."""

    # Extraction de tous les enregistrements de la table Filiere sans filtre ni limite
    # .all() : génère un SELECT * FROM academics_filiere en SQL
    # L'ordre d'affichage dépend du Meta.ordering défini dans le modèle Filiere (si défini)
    filieres = Filiere.objects.all()

    # Rendu du template du catalogue avec injection du QuerySet des filières
    # 'filieres' : variable accessible dans le template via {% for filiere in filieres %}
    return render(request, 'core/formations.html', {'filieres': filieres})


# ==========================================
# VUES DÉDIÉES AUX PAGES INSTITUTIONNELLES
# ==========================================

# Vue de la page de présentation des missions de l'établissement
# Réutilise le même template que la vue about() pour éviter la duplication de fichier HTML
def presentation(request):
    """Redirige et affiche le contenu éditorial des missions (réutilise le template about.html)."""
    # Rendu du template about.html : même template que la vue about()
    # Choix architectural : une seule source HTML pour deux routes URL différentes
    return render(request, 'core/about.html')


# Vue de la page retraçant l'historique de la fondation de l'établissement
def historique(request):
    """Affiche l'historique de la fondation de l'établissement."""
    # Rendu statique : le contenu historique est directement dans le template HTML
    return render(request, 'core/historique.html')


# Vue de la page présentant l'organigramme et les membres dirigeants de l'établissement
def equipe(request):
    """Affiche l'organigramme et les membres du corps enseignant et administratif dirigeant."""
    # Rendu statique : les informations sur l'équipe sont directement dans le template HTML
    # Dans une version avancée, on pourrait injecter ici des données depuis un modèle 'MembreEquipe'
    return render(request, 'core/equipe.html')