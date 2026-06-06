# Fichier à enregistrer sous : dashboard/decorators.py
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

def enseignant_requis(view_func):
    """
    Verrou de sécurité strict (RBAC) pour l'espace enseignant.
    Bloque les étudiants et redirige les utilisateurs anonymes.
    """
    def _wrapped_view(request, *args, **kwargs):
        # 1. Si l'utilisateur n'est pas connecté du tout, on le renvoie au login
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        
        # 2. Si c'est un enseignant, un administrateur ou un superutilisateur, on valide l'accès
        if request.user.role_user == 'ENSEIGNANT' or request.user.is_superuser or request.user.role_user == 'ADMIN':
            return view_func(request, *args, **kwargs)
        
        # 3. Si c'est un étudiant qui tente de forcer l'URL, on lui lève une erreur 403 (Interdit)
        raise PermissionDenied
    return _wrapped_view
