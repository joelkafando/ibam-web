# Importation de LoginView : vue de connexion native de Django
# Gère automatiquement la validation du formulaire, la vérification du mot de passe
# et la création de la session utilisateur après authentification réussie
from django.contrib.auth.views import LoginView

# Importation de reverse_lazy : version différée de reverse() pour résoudre les URLs
# 'lazy' (paresseux) car l'URL est résolue uniquement au moment de l'exécution, pas à l'import
# Indispensable dans les classes (attributs de classe évalués avant le chargement complet des URLs)
from django.urls import reverse_lazy

# Importation des fonctions utilitaires de Django pour le rendu HTML et les redirections
from django.shortcuts import render, redirect

# Importation du décorateur qui bloque l'accès à une vue si l'utilisateur n'est pas connecté
# Redirige automatiquement vers la page de login définie dans settings.py (LOGIN_URL)
from django.contrib.auth.decorators import login_required

# Importation du système de messages flash Django
# Permet d'afficher des notifications (succès, erreur, info) sur la page suivante après une redirection
from django.contrib import messages

# Importation des deux formulaires personnalisés de l'application accounts
# EtudiantRegisterForm : formulaire d'inscription d'un nouvel étudiant
# ModifierProfilEtudiantForm : formulaire de modification des informations personnelles
from .forms import EtudiantRegisterForm, ModifierProfilEtudiantForm


# ==========================================
# 1. CLASSE : CONNEXION PERSONNALISÉE (LOGIN)
# ==========================================

# Définition d'une vue basée sur une classe (Class-Based View) qui hérite de LoginView
# LoginView native gère déjà : affichage du formulaire, vérification des identifiants,
# création de la session et redirection — on surcharge uniquement la logique de redirection
class IBAMLoginView(LoginView):
    """
    Gère l'authentification sécurisée des utilisateurs.
    Analyse le profil du compte après connexion pour le rediriger vers son espace dédié.
    """

    # Attribut de classe : chemin vers le template HTML du formulaire de connexion
    # Django cherchera ce fichier dans les dossiers 'templates' de chaque application installée
    template_name = 'accounts/login.html'

    # Surcharge de la méthode qui détermine l'URL de redirection après une connexion réussie
    # Remplace le comportement par défaut (redirection vers LOGIN_REDIRECT_URL dans settings.py)
    def get_success_url(self):
        """
        Surcharge de la méthode de redirection post-connexion.
        Détermine l'URL de destination de manière dynamique selon le rôle de l'utilisateur.
        """
        # Récupération de l'objet utilisateur connecté depuis la requête HTTP courante
        # request.user est automatiquement rempli par Django après authentification réussie
        user = self.request.user

        # CAS 1 : L'utilisateur est superutilisateur (compte créé via createsuperuser)
        # OU possède explicitement le rôle 'ADMIN' dans le champ role_user
        # is_superuser : booléen natif Django donnant tous les droits sans restriction
        if user.is_superuser or user.role_user == 'ADMIN':
            # reverse_lazy résout le nom de route 'admin_dashboard' de l'espace de noms 'dashboard'
            # Équivalent de l'URL nommée {% url 'dashboard:admin_dashboard' %} dans les templates
            return reverse_lazy('dashboard:admin_dashboard')

        # CAS 2 : L'utilisateur possède le rôle 'ENSEIGNANT'
        # Redirection vers l'espace de gestion dédié aux professeurs
        elif user.role_user == 'ENSEIGNANT':
            return reverse_lazy('dashboard:teacher_dashboard')

        # CAS 3 : Tous les autres rôles (ETUDIANT, ALUMNI) ou cas non prévus
        # Redirection par défaut vers l'espace étudiant (tableau de bord générique)
        else:
            return reverse_lazy('dashboard:student_dashboard')


# ==========================================
# 2. VUE : INSCRIPTION AUTONOME DES ÉTUDIANTS
# ==========================================

# Vue fonction classique (Function-Based View) accessible sans authentification
# Un visiteur non connecté doit pouvoir créer son compte librement
def register_student(request):
    """
    Prend en charge la création de compte par les nouveaux étudiants.
    Injecte automatiquement la filière et le niveau d'études saisis.
    """
    # Vérification de la méthode HTTP de la requête entrante
    # POST : l'utilisateur a soumis le formulaire rempli
    if request.method == 'POST':

        # Instanciation du formulaire en lui transmettant les données soumises via le formulaire HTML
        # request.POST : dictionnaire contenant toutes les valeurs saisies dans le formulaire
        form = EtudiantRegisterForm(request.POST)

        # Déclenchement de toutes les validations définies dans le formulaire et le modèle
        # Vérifie : champs requis remplis, format email valide, mots de passe identiques et robustes...
        if form.is_valid():

            # Sauvegarde de l'utilisateur en base de données via la méthode save() surchargée
            # Injecte automatiquement role_user='ETUDIANT', filiere et niveau_etude
            form.save()

            # Redirection vers la page de connexion après inscription réussie
            # 'accounts:login' : nom de route avec l'espace de noms 'accounts'
            return redirect('accounts:login')

    # Méthode GET : premier affichage de la page d'inscription (formulaire vide)
    else:
        # Instanciation d'un formulaire vide sans données pré-remplies
        form = EtudiantRegisterForm()

    # Rendu du template d'inscription avec transmission du formulaire (vide ou avec erreurs)
    # Si le formulaire était invalide, Django réaffiche la page avec les messages d'erreur intégrés
    return render(request, 'accounts/register.html', {'form': form})
    #                                                  ^ Clé 'form' accessible dans le template via {{ form }}


# ==========================================
# 3. VUE : MODIFICATION DU PROFIL CONNECTÉ
# ==========================================

# Décorateur de protection : redirige vers la page de login si l'utilisateur n'est pas authentifié
# Empêche un visiteur anonyme d'accéder à la page de modification de profil via l'URL directe
@login_required
def modifier_mon_profil(request):
    """
    Permet à l'utilisateur actuellement connecté de mettre à jour ses données de base.
    Met à jour directement la ligne correspondante en base de données sans recréer de compte.
    """
    # Vérification de la méthode HTTP : POST signifie que l'utilisateur a soumis ses modifications
    if request.method == 'POST':

        # Instanciation du formulaire avec les nouvelles données soumises ET l'utilisateur existant
        # request.POST : nouvelles valeurs saisies par l'utilisateur dans le formulaire
        # instance=request.user : indique à Django de MODIFIER cet utilisateur existant
        #                         sans instance, Django créerait un nouvel enregistrement au lieu de mettre à jour
        form = ModifierProfilEtudiantForm(request.POST, instance=request.user)

        # Validation des nouvelles données soumises (format email, champs requis, etc.)
        if form.is_valid():

            # Sauvegarde des modifications : génère un UPDATE SQL sur la ligne de l'utilisateur connecté
            form.save()

            # Création d'un message flash de succès stocké en session
            # Il sera affiché sur la page suivante après la redirection (pattern POST-Redirect-GET)
            messages.success(request, "Vos informations personnelles ont été mises à jour avec succès !")

            # Redirection vers la même page après succès
            # Pattern PRG (Post/Redirect/Get) : évite la re-soumission du formulaire si l'utilisateur
            # recharge la page (F5) après une modification réussie
            return redirect('accounts:modifier_profil')

    # Méthode GET : affichage initial du formulaire pré-rempli avec les données actuelles
    else:
        # Instanciation du formulaire avec les données existantes de l'utilisateur connecté
        # instance=request.user : pré-remplit automatiquement tous les champs avec les valeurs en base
        form = ModifierProfilEtudiantForm(instance=request.user)

    # Rendu du template de modification de profil avec transmission du formulaire
    # Le formulaire est soit vide avec erreurs (POST invalide) soit pré-rempli (GET initial)
    return render(request, 'accounts/modifier_profil.html', {'form': form})
    #                                                         ^ Clé 'form' utilisable dans le template via {{ form }}