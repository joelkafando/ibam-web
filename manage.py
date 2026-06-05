#!/usr/bin/env python
"""
Utilitaire de ligne de commande Django pour les tâches administratives.
Permet d'exécuter des actions comme 'runserver', 'migrate', 'createsuperuser', etc.
"""
import os
import sys


def main():
    """Fonction principale orchestrant le démarrage des commandes d'administration."""
    
    # ÉTAPE 1 : Définition de la variable d'environnement vers le fichier de configuration global du projet.
    # Indique à Django où trouver le fichier 'settings.py' (situé ici dans le dossier 'config')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        # ÉTAPE 2 : Importation de l'exécuteur de commandes natif du cœur de Django
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # CAS D'ANOMALIE : Le framework n'est pas détecté dans l'environnement d'exécution de la machine
        raise ImportError(
            "Impossible d'importer Django. Êtes-vous sûr qu'il est installé et "
            "disponible sur votre variable d'environnement PYTHONPATH ? "
            "Avez-vous oublié d'activer votre environnement virtuel (venv) ?"
        ) from exc
        
    # ÉTAPE 3 : Transmission des arguments tapés par le développeur (sys.argv) au moteur Django
    # Exemple : si vous tapez 'python manage.py runserver', sys.argv contient ['manage.py', 'runserver']
    execute_from_command_line(sys.argv)


# Point d'entrée standard en Python : s'assure que le script est exécuté directement et non importé
if __name__ == '__main__':
    main()
