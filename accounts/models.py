from django.contrib.auth.models import AbstractUser
from django.db import models
from academics.models import Filiere

class Utilisateur(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrateur'),
        ('ENSEIGNANT', 'Enseignant'),
        ('ETUDIANT', 'Étudiant'),
        ('ALUMNI', 'Alumni'),
    ]

    CHOICES_NIVEAU = [
        ('Licence 1', 'Licence 1'),
        ('Licence 2', 'Licence 2'),
        ('Licence 3', 'Licence 3'),
        ('Master 1', 'Master 1'),
        ('Master 2', 'Master 2'),
    ]
    
    role_user = models.CharField(max_length=20, choices=ROLE_CHOICES, default='ETUDIANT', verbose_name="Rôle")
    
    filiere = models.ForeignKey(
        Filiere, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='utilisateurs',
        verbose_name="Filière"
    )
    
    # Résolution du Problème N°2 : Ajout du champ pour le filtrage strict des flux étudiants
    niveau_etude = models.CharField(
        max_length=20, 
        choices=CHOICES_NIVEAU, 
        null=True, 
        blank=True, 
        verbose_name="Niveau d'études (Étudiants)"
    )
    
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role_user = 'ADMIN'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.get_role_user_display()})"
