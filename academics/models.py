from django.db import models
from django.conf import settings # Importation pour cibler proprement votre modèle utilisateur Utilisateur

# ==========================================
# 1. MODÈLE : FILIÈRE
# ==========================================
class Filiere(models.Model):
    # Identifiant unique de la filière (clé primaire auto-incrémentée)
    id_filiere = models.AutoField(primary_key=True)
    
    # Nom de la formation (ex: Informatique, Gestion)
    nom_filiere = models.CharField(max_length=200)
    
    # Niveau global de la formation (ex: Licence, Master)
    niveau = models.CharField(max_length=100)
    
    # Description détaillée du programme de la filière
    description = models.TextField()
    
    # Durée totale du cursus (ex: 3 ans, 2 ans)
    duree = models.CharField(max_length=50)
    
    # Critères requis pour intégrer cette filière
    condition_acces = models.TextField()
    
    # Opportunités professionnelles après l'obtention du diplôme
    debouches = models.TextField()

    # Représentation textuelle de l'objet (utilisée dans l'interface admin)
    def __str__(self):
        return f"{self.nom_filiere} ({self.niveau})"


# ==========================================
# 2. MODÈLE : EMPLOI DU TEMPS
# ==========================================
class EmploiDuTemps(models.Model):
    # Options fixes pour les jours de la semaine (Code, Label affiché)
    JOURS_DE_LA_SEMAINE = [
        ('LUNDI', 'Lundi'),
        ('MARDI', 'Mardi'),
        ('MERCREDI', 'Mercredi'),
        ('JEUDI', 'Jeudi'),
        ('VENDREDI', 'Vendredi'),
        ('SAMEDI', 'Samedi'),
    ]

    # Options fixes pour cibler l'année d'étude exacte
    CHOICES_NIVEAU = [
        ('Licence 1', 'Licence 1'),
        ('Licence 2', 'Licence 2'),
        ('Licence 3', 'Licence 3'),
        ('Master 1', 'Master 1'),
        ('Master 2', 'Master 2'),
    ]

    # Relation clé étrangère liée au modèle Filiere (Suppression en cascade si la filière est supprimée)
    filiere = models.ForeignKey(
        'Filiere', 
        on_delete=models.CASCADE, 
        related_name='emplois_du_temps', 
        verbose_name="Filière"
    )

    # Menu déroulant pour spécifier la classe concernée
    niveau_etude = models.CharField(
        max_length=20, 
        choices=CHOICES_NIVEAU, 
        verbose_name="Niveau d'études", 
        default="Licence 1"
    )
        
    # Saisie libre pour désigner la semaine concernée par ce cours
    semaine_du = models.CharField(
        max_length=100, 
        verbose_name="Période / Semaine", 
        default="Semaine en cours",
        help_text="Ex: Du 25 au 30 mai 2026"
    )
    
    # Informations sur le cours, l'intervenant et le lieu
    nom_matiere = models.CharField(max_length=150, verbose_name="Matière")
    
    enseignant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role_user': 'ENSEIGNANT'},
        related_name='cours_planifies',
        verbose_name="Enseignant"
    )
    
    # Menu déroulant basé sur la liste JOURS_DE_LA_SEMAINE
    jour = models.CharField(max_length=10, choices=JOURS_DE_LA_SEMAINE, verbose_name="Jour de la semaine")
    
    # Créneaux horaires du cours
    heure_debut = models.TimeField(verbose_name="Heure de début")
    heure_fin = models.TimeField(verbose_name="Heure de fin")
    
    # Nom ou numéro de la pièce où se déroule le cours
    salle = models.CharField(max_length=50, verbose_name="Salle de cours")

    # Options de configuration du modèle
    class Meta:
        verbose_name = "Emploi du temps"              # Nom au singulier dans l'admin
        verbose_name_plural = "Emplois du temps"      # Nom au pluriel dans l'admin
        ordering = ['jour', 'heure_debut']            # Tri automatique par jour puis par heure

    # Représentation textuelle de l'entrée d'emploi du temps
    def __str__(self):
        return f"{self.filiere.nom_filiere} - {self.nom_matiere} ({self.jour})"

# ==========================================
# 3. MODÈLE : BIBLIOTHÈQUE / RESSOURCES (CONFORME CDC 2.2.4)
# ==========================================
class RessourcePedagogique(models.Model):
    """
    Permet aux enseignants de téléverser des supports de cours (PDF, Docs).
    Lien dynamique avec les filières et niveaux d'études de l'IBAM.
    """
    enseignant = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='ressources_deposees',
        verbose_name="Enseignant"
    )
    filiere = models.ForeignKey(
        Filiere, 
        on_delete=models.CASCADE, 
        related_name='ressources_pedagogiques',
        verbose_name="Filière ciblée"
    )
    # Réutilisation de votre liste de choix existante CHOICES_NIVEAU
    niveau_etude = models.CharField(
        max_length=20, 
        choices=EmploiDuTemps.CHOICES_NIVEAU, 
        verbose_name="Niveau d'études ciblé"
    )
    titre_cours = models.CharField(max_length=150, verbose_name="Titre du support de cours")
    
    # Champ de téléversement réel (les fichiers seront stockés dans le dossier media/cours_supports/)
    fichier = models.FileField(upload_to='cours_supports/', verbose_name="Fichier du cours (PDF, Word, etc.)")
    date_depot = models.DateTimeField(auto_now_add=True, verbose_name="Date de dépôt")

    class Meta:
        verbose_name = "Ressource Pédagogique"
        verbose_name_plural = "Ressources Pédagogiques"
        ordering = ['-date_depot']

    def __str__(self):
        return f"{self.titre_cours} - {self.filiere.nom_filiere} ({self.niveau_etude})"


# ==========================================
# 4. MODÈLE : DISPONIBILITÉS ENSEIGNANTS (CONFORME CDC 2.2.2)
# ==========================================
class DisponibiliteEnseignant(models.Model):
    """
    Permet aux professeurs de soumettre leurs créneaux libres à l'administration
    pour faciliter la conception des emplois du temps.
    """
    CHOICES_PERIODE = [
        ('MATIN', 'Matin (07h00 - 12h00)'),
        ('APRES_MIDI', 'Après-midi (13h00 - 18h00)'),
        ('JOURNEE', 'Journée complète'),
    ]

    enseignant = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='disponibilites_soumises',
        verbose_name="Enseignant"
    )
    # Réutilisation de votre liste de choix existante JOURS_DE_LA_SEMAINE
    jour = models.CharField(
        max_length=10, 
        choices=EmploiDuTemps.JOURS_DE_LA_SEMAINE, 
        verbose_name="Jour proposé"
    )
    periode = models.CharField(
        max_length=15, 
        choices=CHOICES_PERIODE, 
        verbose_name="Créneau horaire"
    )
    note_complementaire = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Précisions ou contraintes particulières",
        help_text="Ex: Seulement libre à partir de 15h00 ce jour-là."
    )
    date_soumission = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Disponibilité Enseignant"
        verbose_name_plural = "Disponibilités Enseignants"
        ordering = ['jour']

    def __str__(self):
        return f"Dispo {self.enseignant.username} - {self.get_jour_display()} ({self.get_periode_display()})"
