from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EtudiantRegisterForm, ModifierProfilEtudiantForm  # Importation des formulaires d'inscription et de modification

# ==========================================
# 1. CLASSE : CONNEXION PERSONNALISÉE (LOGIN)
# ==========================================
class IBAMLoginView(LoginView):
    """
    Gère l'authentification sécurisée des utilisateurs.
    Analyse le profil du compte après connexion pour le rediriger vers son espace dédié.
    """
    # Chemin vers le fichier HTML contenant le formulaire de connexion
    template_name = 'accounts/login.html'
    
    def get_success_url(self):
        """
        Surcharge de la méthode de redirection post-connexion.
        Détermine l'URL de destination de manière dynamique selon le rôle de l'utilisateur.
        """
        user = self.request.user
        
        # CAS 1 : Redirection vers le tableau de bord de l'administrateur
        if user.is_superuser or user.role_user == 'ADMIN':
            return reverse_lazy('dashboard:admin_dashboard')
            
        # CAS 2 : Redirection vers l'espace enseignant
        elif user.role_user == 'ENSEIGNANT':
            return reverse_lazy('dashboard:teacher_dashboard')
            
        # CAS 3 : Redirection par défaut vers l'espace étudiant ou alumni
        else:
            return reverse_lazy('dashboard:student_dashboard')


# ==========================================
# 2. VUE : INSCRIPTION AUTONOME DES ÉTUDIANTS
# ==========================================
def register_student(request):
    """
    Prend en charge la création de compte par les nouveaux étudiants.
    Injecte automatiquement la filière et le niveau d'études saisis.
    """
    # Traitement de la soumission du formulaire (Méthode POST)
    if request.method == 'POST':
        form = EtudiantRegisterForm(request.POST)
        
        # Vérification de la conformité des données (mots de passe identiques, champs remplis...)
        if form.is_valid():
            form.save()  # Enregistrement du nouvel utilisateur en base de données
            return redirect('accounts:login')  # Redirection immédiate vers l'écran de connexion
            
    # Affichage initial du formulaire vide (Méthode GET)
    else:
        form = EtudiantRegisterForm()
    
    # Rendu graphique de la page d'inscription avec l'objet formulaire
    return render(request, 'accounts/register.html', {'form': form})


# ==========================================
# 3. VUE : MODIFICATION DU PROFIL CONNECTÉ
# ==========================================
@login_required  # Sécurité : Bloque l'accès à la page si l'utilisateur n'est pas authentifié
def modifier_mon_profil(request):
    """
    Permet à l'utilisateur actuellement connecté de mettre à jour ses données de base.
    Met à jour directement la ligne correspondante en base de données sans recréer de compte.
    """
    # Traitement de la mise à jour des données (Méthode POST)
    if request.method == 'POST':
        # L'argument instance=request.user indique à Django de modifier l'utilisateur connecté actuel
        form = ModifierProfilEtudiantForm(request.POST, instance=request.user)
        
        if form.is_valid():
            form.save()  # Application des modifications en base de données
            
            # Stockage d'un message d'alerte positif destiné à être affiché sur le template
            messages.success(request, "Vos informations personnelles ont été mises à jour avec succès !")
            
            # Redirection sur la même page pour vider le cache POST et afficher le message de succès
            return redirect('accounts:modifier_profil')
            
    # Affichage initial de la page avec les champs pré-remplis par les données de l'utilisateur (Méthode GET)
    else:
        form = ModifierProfilEtudiantForm(instance=request.user)
        
    # Rendu graphique de la page de gestion de profil
    return render(request, 'accounts/modifier_profil.html', {'form': form})
