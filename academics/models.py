# Importation du module models de Django pour définir les modèles de base de données
from django.db import models

# Importation de settings pour référencer le modèle utilisateur de manière flexible
# (évite de coder en dur le modèle User et respecte les bonnes pratiques Django)
from django.conf import settings


# ==========================================
# 1. MODÈLE : FILIÈRE
# ==========================================

# Définition du modèle Filiere qui hérite de models.Model (classe de base Django)
class Filiere(models.Model):

    # Clé primaire auto-incrémentée : chaque filière aura un identifiant unique généré automatiquement
    id_filiere = models.AutoField(primary_key=True)

    # Champ texte court pour stocker le nom de la filière (ex: "Informatique", "Gestion")
    # max_length=200 : longueur maximale de 200 caractères
    nom_filiere = models.CharField(max_length=200)

    # Champ texte court pour le niveau global de la formation (ex: "Licence", "Master")
    niveau = models.CharField(max_length=100)

    # Champ texte long (sans limite de caractères) pour la description complète du programme
    description = models.TextField()

    # Champ texte court pour la durée totale du cursus (ex: "3 ans", "2 ans")
    duree = models.CharField(max_length=50)

    # Champ texte long pour décrire les prérequis nécessaires pour intégrer la filière
    condition_acces = models.TextField()

    # Champ texte long pour lister les débouchés professionnels après obtention du diplôme
    debouches = models.TextField()

    # Méthode spéciale Python qui définit la représentation textuelle d'un objet Filiere
    # Utilisée dans l'interface admin et partout où l'objet est affiché sous forme de texte
    def __str__(self):
        # Retourne une chaîne formatée : ex → "Informatique (Licence)"
        return f"{self.nom_filiere} ({self.niveau})"


# ==========================================
# 2. MODÈLE : EMPLOI DU TEMPS
# ==========================================

# Définition du modèle EmploiDuTemps qui hérite de models.Model
class EmploiDuTemps(models.Model):

    # Liste de tuples définissant les choix valides pour les jours de la semaine
    # Format : ('valeur_stockée_en_BDD', 'Label affiché à l'utilisateur')
    JOURS_DE_LA_SEMAINE = [
        ('LUNDI', 'Lundi'),       # Lundi : stocké 'LUNDI' en base de données
        ('MARDI', 'Mardi'),       # Mardi : stocké 'MARDI' en base de données
        ('MERCREDI', 'Mercredi'), # Mercredi : stocké 'MERCREDI' en base de données
        ('JEUDI', 'Jeudi'),       # Jeudi : stocké 'JEUDI' en base de données
        ('VENDREDI', 'Vendredi'), # Vendredi : stocké 'VENDREDI' en base de données
        ('SAMEDI', 'Samedi'),     # Samedi : stocké 'SAMEDI' en base de données
    ]

    # Liste de tuples définissant les niveaux d'études disponibles
    # Réutilisable ailleurs dans le projet (ex: dans RessourcePedagogique)
    CHOICES_NIVEAU = [
        ('Licence 1', 'Licence 1'), # Première année de Licence
        ('Licence 2', 'Licence 2'), # Deuxième année de Licence
        ('Licence 3', 'Licence 3'), # Troisième année de Licence
        ('Master 1', 'Master 1'),   # Première année de Master
        ('Master 2', 'Master 2'),   # Deuxième année de Master
    ]

    # Clé étrangère vers le modèle Filiere
    # on_delete=CASCADE : si la filière est supprimée, tous ses emplois du temps le sont aussi
    # related_name : permet d'accéder aux emplois du temps depuis une filière via filiere.emplois_du_temps.all()
    # verbose_name : label affiché dans l'interface d'administration
    filiere = models.ForeignKey(
        'Filiere',                          # Référence au modèle Filiere (en chaîne pour éviter les imports circulaires)
        on_delete=models.CASCADE,           # Suppression en cascade si la filière parente est supprimée
        related_name='emplois_du_temps',    # Nom du lien inverse pour accéder depuis Filiere
        verbose_name="Filière"              # Label affiché dans l'admin Django
    )

    # Champ de sélection pour le niveau d'étude de la classe concernée
    # choices=CHOICES_NIVEAU : restreint les valeurs possibles à la liste définie plus haut
    # default="Licence 1" : valeur pré-remplie si aucune n'est saisie
    niveau_etude = models.CharField(
        max_length=20,                      # Longueur max suffisante pour "Licence 1" à "Master 2"
        choices=CHOICES_NIVEAU,             # Menu déroulant basé sur la liste CHOICES_NIVEAU
        verbose_name="Niveau d'études",     # Label dans l'admin
        default="Licence 1"                 # Valeur par défaut à la création d'un enregistrement
    )

    # Champ texte court pour identifier la semaine concernée par cet emploi du temps
    # help_text : indice affiché sous le champ dans le formulaire admin
    semaine_du = models.CharField(
        max_length=100,                             # Longueur suffisante pour une description de semaine
        verbose_name="Période / Semaine",           # Label dans l'admin
        default="Semaine en cours",                 # Valeur pré-remplie par défaut
        help_text="Ex: Du 25 au 30 mai 2026"        # Exemple indicatif affiché sous le champ
    )

    # Champ texte court pour le nom de la matière enseignée (ex: "Mathématiques", "Algorithmique")
    nom_matiere = models.CharField(max_length=150, verbose_name="Matière")

    # Clé étrangère vers le modèle utilisateur défini dans settings.AUTH_USER_MODEL
    # limit_choices_to : filtre les utilisateurs pour n'afficher que ceux ayant le rôle 'ENSEIGNANT'
    # related_name : accès inverse depuis l'utilisateur → user.cours_planifies.all()
    enseignant = models.ForeignKey(
        settings.AUTH_USER_MODEL,                       # Référence au modèle User personnalisé du projet
        on_delete=models.CASCADE,                       # Suppression en cascade si l'utilisateur est supprimé
        limit_choices_to={'role_user': 'ENSEIGNANT'},   # Restreint les choix aux utilisateurs enseignants
        related_name='cours_planifies',                 # Nom du lien inverse depuis le modèle utilisateur
        verbose_name="Enseignant"                       # Label affiché dans l'interface admin
    )

    # Champ de sélection pour le jour du cours parmi les jours définis dans JOURS_DE_LA_SEMAINE
    jour = models.CharField(
        max_length=10,                          # Longueur max pour stocker les codes comme 'MERCREDI'
        choices=JOURS_DE_LA_SEMAINE,            # Menu déroulant basé sur la liste des jours
        verbose_name="Jour de la semaine"       # Label dans l'admin
    )

    # Champ horaire pour l'heure de début du cours (format HH:MM:SS en base de données)
    heure_debut = models.TimeField(verbose_name="Heure de début")

    # Champ horaire pour l'heure de fin du cours
    heure_fin = models.TimeField(verbose_name="Heure de fin")

    # Champ texte court pour le nom ou numéro de la salle (ex: "Salle A12", "Amphi 2")
    salle = models.CharField(max_length=50, verbose_name="Salle de cours")

    # Classe interne Meta : configure les options globales du modèle
    class Meta:
        verbose_name = "Emploi du temps"         # Nom singulier affiché dans l'interface admin
        verbose_name_plural = "Emplois du temps" # Nom pluriel affiché dans l'interface admin
        ordering = ['jour', 'heure_debut']       # Tri automatique : d'abord par jour, puis par heure de début

    # Représentation textuelle d'un objet EmploiDuTemps
    def __str__(self):
        # Retourne ex → "Informatique - Algorithmique (LUNDI)"
        return f"{self.filiere.nom_filiere} - {self.nom_matiere} ({self.jour})"


# ==========================================
# 3. MODÈLE : BIBLIOTHÈQUE / RESSOURCES
# ==========================================

# Modèle permettant aux enseignants de déposer des supports de cours (PDF, Word, etc.)
class RessourcePedagogique(models.Model):
    """
    Permet aux enseignants de téléverser des supports de cours (PDF, Docs).
    Lien dynamique avec les filières et niveaux d'études.
    """

    # Clé étrangère vers le modèle utilisateur : identifie l'enseignant ayant déposé la ressource
    # related_name : accès inverse → user.ressources_deposees.all()
    enseignant = models.ForeignKey(
        settings.AUTH_USER_MODEL,           # Modèle User personnalisé du projet
        on_delete=models.CASCADE,           # Supprime les ressources si l'enseignant est supprimé
        related_name='ressources_deposees', # Nom du lien inverse depuis le modèle User
        verbose_name="Enseignant"           # Label dans l'admin
    )

    # Clé étrangère vers la filière concernée par cette ressource pédagogique
    # related_name : accès inverse → filiere.ressources_pedagogiques.all()
    filiere = models.ForeignKey(
        Filiere,                                    # Référence directe au modèle Filiere (déjà défini)
        on_delete=models.CASCADE,                   # Supprime les ressources si la filière est supprimée
        related_name='ressources_pedagogiques',     # Nom du lien inverse depuis Filiere
        verbose_name="Filière ciblée"               # Label dans l'admin
    )

    # Champ de sélection pour le niveau d'études ciblé par la ressource
    # Réutilise la liste CHOICES_NIVEAU définie dans EmploiDuTemps pour éviter la duplication
    niveau_etude = models.CharField(
        max_length=20,
        choices=EmploiDuTemps.CHOICES_NIVEAU,   # Réutilisation de la liste de choix existante
        verbose_name="Niveau d'études ciblé"    # Label dans l'admin
    )

    # Champ texte court pour le titre du support de cours (ex: "Cours Algorithmique - Chapitre 1")
    titre_cours = models.CharField(max_length=150, verbose_name="Titre du support de cours")

    # Champ de téléversement de fichier : stocke le chemin relatif du fichier en base de données
    # upload_to : sous-dossier dans MEDIA_ROOT où les fichiers seront physiquement enregistrés
    fichier = models.FileField(
        upload_to='cours_supports/',                    # Chemin de stockage → media/cours_supports/
        verbose_name="Fichier du cours (PDF, Word, etc.)" # Label dans l'admin
    )

    # Champ date/heure rempli automatiquement à la création de l'enregistrement
    # auto_now_add=True : la date est définie une seule fois à la création, jamais modifiée ensuite
    date_depot = models.DateTimeField(auto_now_add=True, verbose_name="Date de dépôt")

    # Classe Meta pour les options globales du modèle RessourcePedagogique
    class Meta:
        verbose_name = "Ressource Pédagogique"          # Nom singulier dans l'admin
        verbose_name_plural = "Ressources Pédagogiques" # Nom pluriel dans l'admin
        ordering = ['-date_depot']                      # Tri par date décroissante (les plus récentes en premier)
        #             ^ le signe '-' signifie ordre décroissant

    # Représentation textuelle d'une ressource pédagogique
    def __str__(self):
        # Retourne ex → "Cours Algo Chapitre 1 - Informatique (Licence 2)"
        return f"{self.titre_cours} - {self.filiere.nom_filiere} ({self.niveau_etude})"


# ==========================================
# 4. MODÈLE : DISPONIBILITÉS ENSEIGNANTS
# ==========================================

# Modèle permettant aux enseignants de soumettre leurs créneaux de disponibilité
class DisponibiliteEnseignant(models.Model):
    """
    Permet aux professeurs de soumettre leurs créneaux libres à l'administration
    pour faciliter la conception des emplois du temps.
    """

    # Liste de tuples définissant les périodes de la journée disponibles
    CHOICES_PERIODE = [
        ('MATIN', 'Matin (07h00 - 12h00)'),         # Créneau du matin
        ('APRES_MIDI', 'Après-midi (13h00 - 18h00)'),# Créneau de l'après-midi
        ('JOURNEE', 'Journée complète'),              # Disponible toute la journée
    ]

    # Clé étrangère vers l'utilisateur (enseignant) ayant soumis sa disponibilité
    # related_name : accès inverse → user.disponibilites_soumises.all()
    enseignant = models.ForeignKey(
        settings.AUTH_USER_MODEL,                   # Modèle User personnalisé du projet
        on_delete=models.CASCADE,                   # Supprime les disponibilités si l'utilisateur est supprimé
        related_name='disponibilites_soumises',     # Nom du lien inverse depuis le modèle User
        verbose_name="Enseignant"                   # Label dans l'admin
    )

    # Champ de sélection pour le jour de disponibilité
    # Réutilise JOURS_DE_LA_SEMAINE d'EmploiDuTemps pour ne pas dupliquer la liste
    jour = models.CharField(
        max_length=10,
        choices=EmploiDuTemps.JOURS_DE_LA_SEMAINE,  # Réutilisation de la liste des jours
        verbose_name="Jour proposé"                 # Label dans l'admin
    )

    # Champ de sélection pour la période de disponibilité (matin, après-midi ou journée)
    periode = models.CharField(
        max_length=15,              # Longueur suffisante pour stocker 'APRES_MIDI'
        choices=CHOICES_PERIODE,    # Menu déroulant basé sur la liste CHOICES_PERIODE
        verbose_name="Créneau horaire" # Label dans l'admin
    )

    # Champ texte optionnel pour des précisions supplémentaires de l'enseignant
    # blank=True : le champ peut être vide dans les formulaires
    # null=True : la valeur NULL est autorisée en base de données (champ non obligatoire)
    # help_text : exemple indicatif affiché sous le champ dans le formulaire
    note_complementaire = models.TextField(
        blank=True,                                             # Champ facultatif dans les formulaires
        null=True,                                              # Valeur NULL autorisée en base de données
        verbose_name="Précisions ou contraintes particulières", # Label dans l'admin
        help_text="Ex: Seulement libre à partir de 15h00 ce jour-là." # Indication contextuelle
    )

    # Champ date/heure rempli automatiquement lors de la soumission de la disponibilité
    # auto_now_add=True : enregistre la date une seule fois à la création, non modifiable ensuite
    date_soumission = models.DateTimeField(auto_now_add=True)

    # Classe Meta pour les options globales du modèle DisponibiliteEnseignant
    class Meta:
        verbose_name = "Disponibilité Enseignant"           # Nom singulier dans l'admin
        verbose_name_plural = "Disponibilités Enseignants"  # Nom pluriel dans l'admin
        ordering = ['jour']                                 # Tri automatique par ordre alphabétique du jour

    # Représentation textuelle d'une disponibilité
    def __str__(self):
        # get_jour_display() : retourne le label lisible du jour (ex: 'LUNDI' → 'Lundi')
        # get_periode_display() : retourne le label lisible de la période (ex: 'MATIN' → 'Matin (07h00 - 12h00)')
        # Retourne ex → "Dispo prof_dupont - Lundi (Matin (07h00 - 12h00))"
        return f"Dispo {self.enseignant.username} - {self.get_jour_display()} ({self.get_periode_display()})"