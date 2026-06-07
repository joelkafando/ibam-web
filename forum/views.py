# Importation des fonctions utilitaires Django pour le rendu, la récupération sécurisée et la redirection
from django.shortcuts import render, get_object_or_404, redirect

# Décorateur qui bloque l'accès aux vues pour les utilisateurs non connectés
from django.contrib.auth.decorators import login_required

# Système de messages flash Django pour afficher des notifications (succès, erreurs)
from django.contrib import messages

# Importation des modèles de données du forum (catégories, sujets, réponses)
from .models import CategorieForum, SujetForum, ReponseForum

# Importation des formulaires de création de sujets et de réponses
from .forms import SujetForumForm, ReponseForumForm


# ==========================================
# VUE : PAGE D'ACCUEIL DU FORUM
# ==========================================

# Restriction d'accès : seuls les membres connectés peuvent accéder au forum
@login_required
def index_forum(request):
    """Affiche la page d'accueil du forum avec les catégories et les derniers sujets."""

    # Récupération de toutes les catégories disponibles dans le forum
    categories = CategorieForum.objects.all()

    # Récupération des 5 discussions les plus récentes (le slice [:5] limite le queryset)
    derniers_sujets = SujetForum.objects.all()[:5]

    # Construction du contexte de données à transmettre au template
    context = {
        # Liste de toutes les catégories pour construire le menu du forum
        'categories': categories,

        # Les 5 dernières discussions pour afficher un aperçu global de l'activité
        'derniers_sujets': derniers_sujets,
    }

    # Rendu du template d'accueil du forum avec les données du contexte
    return render(request, 'forum/index_forum.html', context)


# ==========================================
# VUE : CRÉER UN SUJET DE DISCUSSION
# ==========================================

# Restriction d'accès : seul un utilisateur connecté peut créer un sujet
@login_required
def creer_sujet(request):
    """Permet à tout utilisateur connecté de publier une nouvelle discussion."""

    # Traitement du formulaire uniquement si la requête est de type POST (soumission)
    if request.method == 'POST':

        # Instanciation du formulaire avec les données envoyées par l'utilisateur
        form = SujetForumForm(request.POST)

        # Vérification que toutes les données saisies sont valides
        if form.is_valid():

            # Création de l'objet en mémoire sans sauvegarde immédiate en base (commit=False)
            # Nécessaire pour pouvoir injecter manuellement l'auteur avant la sauvegarde
            sujet = form.save(commit=False)

            # Injection de l'utilisateur connecté comme auteur du sujet
            sujet.auteur = request.user

            # Sauvegarde définitive du sujet en base de données
            sujet.save()

            # Affichage d'un message de confirmation visible dans le template
            messages.success(request, "Votre sujet a été publié avec succès !")

            # Redirection vers la page de détail du sujet nouvellement créé
            # "pk=sujet.pk" passe l'identifiant du sujet à l'URL (pattern PRG)
            return redirect('forum:detail_sujet', pk=sujet.pk)

    else:
        # Si la requête est GET (simple visite de la page), on affiche un formulaire vide
        form = SujetForumForm()

    # Rendu du template avec le formulaire (vide ou avec erreurs selon le cas)
    return render(request, 'forum/creer_sujet.html', {'form': form})


# ==========================================
# VUE : LIRE UN SUJET ET AJOUTER UNE RÉPONSE
# ==========================================

# Restriction d'accès : seul un utilisateur connecté peut lire et répondre
@login_required
def detail_sujet(request, pk):
    """Affiche une discussion complète et traite l'envoi de nouvelles réponses."""

    # Récupération du sujet correspondant à l'identifiant "pk" passé dans l'URL
    # Si aucun sujet ne correspond, Django renvoie automatiquement une erreur 404
    sujet = get_object_or_404(SujetForum, pk=pk)

    # Récupération de toutes les réponses liées à ce sujet
    # "sujet.reponses" fonctionne grâce au related_name='reponses' défini dans le modèle ReponseForum
    reponses = sujet.reponses.all()

    # Traitement du formulaire de réponse uniquement si la requête est de type POST
    if request.method == 'POST':

        # Instanciation du formulaire avec les données soumises par l'utilisateur
        form = ReponseForumForm(request.POST)

        # Vérification de la validité des données saisies
        if form.is_valid():

            # Création de l'objet réponse en mémoire sans sauvegarde immédiate
            # Permet d'injecter le sujet et l'auteur avant la sauvegarde définitive
            reponse = form.save(commit=False)

            # Liaison de la réponse au sujet actuellement consulté
            reponse.sujet = sujet

            # Injection de l'utilisateur connecté comme auteur de la réponse
            reponse.auteur = request.user

            # Sauvegarde définitive de la réponse en base de données
            reponse.save()

            # Message de confirmation affiché après l'ajout de la réponse
            messages.success(request, "Votre réponse a été ajoutée !")

            # Redirection vers la même page de détail pour éviter la re-soumission (pattern PRG)
            return redirect('forum:detail_sujet', pk=sujet.pk)

    else:
        # Si la requête est GET, on affiche un formulaire de réponse vide
        form = ReponseForumForm()

    # Construction du contexte avec toutes les données nécessaires au template
    context = {
        # L'objet sujet complet (titre, auteur, contenu, date...)
        'sujet': sujet,

        # Le queryset de toutes les réponses associées à ce sujet
        'reponses': reponses,

        # Le formulaire de réponse (vide ou avec erreurs de validation)
        'form': form,
    }

    # Rendu du template de détail avec le contexte complet
    return render(request, 'forum/detail_sujet.html', context)


# ==========================================
# VUE : SUJETS PAR CATÉGORIE
# ==========================================

# Restriction d'accès : navigation dans les catégories réservée aux membres connectés
@login_required
def sujets_par_categorie(request, pk):
    """Affiche tous les sujets de discussion liés à une catégorie spécifique."""

    # Récupération de la catégorie correspondant à l'identifiant "pk" de l'URL
    # Renvoie automatiquement une erreur 404 si la catégorie n'existe pas en base
    categorie = get_object_or_404(CategorieForum, pk=pk)

    # Récupération de tous les sujets liés à cette catégorie via le related_name='sujets'
    # Tri : les sujets épinglés apparaissent en premier (-est_epinglé),
    # puis classés du plus récent au plus ancien (-date_creation)
    sujets = categorie.sujets.all().order_by('-est_epinglé', '-date_creation')

    # Construction du contexte avec la catégorie et ses sujets filtrés
    context = {
        # La catégorie sélectionnée (nom, description...) pour l'afficher dans le template
        'categorie': categorie,

        # Le queryset des sujets filtrés et triés pour cette catégorie
        'sujets': sujets,
    }

    # Rendu du template de liste des sujets par catégorie
    return render(request, 'forum/sujets_par_categorie.html', context)