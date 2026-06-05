from django.shortcuts import render
from django.db.models import Q
from academics.models import Filiere  # Importation depuis votre application academics
from accounts.models import User      # Importation de votre modèle utilisateur personnalisé
from django.contrib.auth.decorators import login_required  # Django gère cela nativement et de façon très puissante grâce au décorateur @login_required


# ==========================================
# VUE : LISTE ET FILTRAGE DES ALUMNI
# ==========================================
@login_required  # <-- Force la connexion avant de voir les profils
def liste_alumni(request):
    """
    Vue filtrant et affichant le réseau des anciens étudiants (Alumni)
    conformément au module 2.2.5 du cahier des charges.
    """
    # 1. Récupération initiale de tous les comptes ayant strictement le rôle 'alumni'
    # Ajustez 'role="alumni"' selon la configuration exacte de votre modèle User personnalisé
    diplomes = User.objects.filter(role='alumni')
    
    # 2. Récupération de l'intégralité des filières pour alimenter le menu déroulant du formulaire
    filieres = Filiere.objects.all()
    
    # 3. Récupération et nettoyage des paramètres de filtrage envoyés par le formulaire HTML (Méthode GET)
    recherche_nom = request.GET.get('q', '').strip()
    filiere_selectionnee_id = request.GET.get('filiere_id', '').strip()
    
    # 4. Application du filtre textuel insensible à la casse si une recherche est soumise
    if recherche_nom:
        # Utilisation de Q pour effectuer une condition OR (OU) sur le prénom, le nom ou le pseudo
        diplomes = diplomes.filter(
            Q(first_name__icontains=recherche_nom) | 
            Q(last_name__icontains=recherche_nom) |
            Q(username__icontains=recherche_nom)
        )
    
    # 5. Application du filtre par clé étrangère si une filière spécifique est sélectionnée
    if filiere_selectionnee_id:
        diplomes = diplomes.filter(filiere_id=filiere_selectionnee_id)
        
    # 6. Construction du dictionnaire de contexte à envoyer pour le rendu de la page
    context = {
        'diplomes': diplomes,                             # Liste finale filtrée des diplômés
        'filieres': filieres,                             # Liste complète des filières pour les filtres
        'recherche_nom': recherche_nom,                   # Terme recherché mémorisé pour réaffichage
        'filiere_selectionnee_id': filiere_selectionnee_id, # ID mémorisé pour conserver la sélection active
    }
    
    # Rendu final du template spécifié avec injection du contexte de données
    return render(request, 'alumni/alumni.html', context)
