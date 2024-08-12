from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class Organisation(models.Model):
    name = models.CharField(max_length=50)
    emailOrganisation = models.EmailField(unique=True)

class Cagnotte(models.Model):
    intitule = models.CharField(max_length=200)
    description = models.TextField(blank=True)  
    image = models.ImageField(upload_to='cagnottes/', blank=True, null=True)  
    montant_collecte = models.FloatField(default=0)
    objectif_montant_vise = models.FloatField()
    date_debut = models.DateField()
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='cagnottes')

    def __str__(self):
        return self.intitule

class Don(models.Model):
    montant = models.FloatField()
    cagnotte = models.ForeignKey(Cagnotte, on_delete=models.CASCADE, related_name='dons')
    donateur = models.ForeignKey('Donateur', on_delete=models.SET_NULL, null=True, blank=True)
    date_don=models.DateField()

    def __str__(self):
        return f"{self.intitule} - {self.montant}€"

class JustificationDon(models.Model):
    motif = models.CharField(max_length=200)
    montant = models.FloatField()
    infos_beneficiaire = models.TextField()
    cagnotte = models.ForeignKey(Cagnotte, on_delete=models.CASCADE, related_name='justifications')
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)  # Modifié pour pointer vers Organisation

    def __str__(self):
        return f"{self.motif} - {self.montant}€"

class Donateur(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return f"{self.prenom} {self.nom}"
