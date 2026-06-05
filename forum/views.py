from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CategorieForum, SujetForum, ReponseForum
from .forms import SujetForumForm, ReponseForumForm

@login_required # Le cahier des charges restreint le forum aux membres authentifiés
def index_forum(request):
    """Affiche la page d'accueil du forum avec les catégories"""
    categories = CategorieForum.objects.all()
    derniers_sujets = SujetForum.objects.all()[:5] # Affiche les 5 dernières discussions globales
    
    context = {
        'categories': categories,
        'derniers_sujets': derniers_sujets,
    }
    return render(request, 'forum/index_forum.html', context)

# ==========================================
# VUE : CRÉER UN SUJET DE DISCUSSION
# ==========================================
@login_required
def creer_sujet(request):
    """Permet à tout utilisateur connecté de publier une nouvelle discussion"""
    if request.method == 'POST':
        form = SujetForumForm(request.POST)
        if form.is_valid():
            # Crée l'objet en mémoire sans le sauvegarder immédiatement pour lui injecter l'auteur
            sujet = form.save(commit=False)
            sujet.auteur = request.user
            sujet.save()
            messages.success(request, "Votre sujet a été publié avec succès !")
            return redirect('forum:detail_sujet', pk=sujet.pk)
    else:
        form = SujetForumForm()
        
    return render(request, 'forum/creer_sujet.html', {'form': form})


# ==========================================
# VUE : LIRE UN SUJET ET AJOUTER UNE RÉPONSE
# ==========================================
@login_required
def detail_sujet(request, pk):
    """Affiche une discussion complète et traite l'envoi de nouvelles réponses"""
    sujet = get_object_or_404(SujetForum, pk=pk)
    reponses = sujet.reponses.all() # Récupère tous les commentaires liés grâce au related_name
    
    if request.method == 'POST':
        form = ReponseForumForm(request.POST)
        if form.is_valid():
            reponse = form.save(commit=False)
            reponse.sujet = sujet
            reponse.auteur = request.user
            reponse.save()
            messages.success(request, "Votre réponse a été ajoutée !")
            return redirect('forum:detail_sujet', pk=sujet.pk)
    else:
        form = ReponseForumForm()
        
    context = {
        'sujet': sujet,
        'reponses': reponses,
        'form': form,
    }
    return render(request, 'forum/detail_sujet.html', context)

@login_required
def sujets_par_categorie(request, pk):
    """Affiche tous les sujets de discussion liés à une catégorie spécifique"""
    # On récupère la catégorie ou on renvoie une erreur 404 si l'identifiant n'existe pas
    categorie = get_object_or_404(CategorieForum, pk=pk)
    
    # On extrait tous les sujets associés à cette catégorie grâce au related_name='sujets'
    sujets = categorie.sujets.all().order_by('-est_epinglé', '-date_creation')
    
    context = {
        'categorie': categorie,
        'sujets': sujets,
    }
    return render(request, 'forum/sujets_par_categorie.html', context)