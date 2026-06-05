from django.db import models

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
    enseignant = models.CharField(max_length=100, verbose_name="Enseignant", help_text="Nom de l'enseignant")
    
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
