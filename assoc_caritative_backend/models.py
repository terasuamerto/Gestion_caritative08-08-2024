from django.db import models

# Create your models here.
class Don(models.Model):
    intituleDon = models.CharField(max_length=200)
    montantDon = models.FloatField()

class Cagnotte(models.Model):
    intituleCagnotte = models.CharField(max_length=200)
    montantCagnotte = models.FloatField()
    objectifMontantVise = models.FloatField()
    dateDebut = models.DateField()
    dateFin = models.DateField()

class JustificationDon(models.Model):
    motif = models.CharField(max_length=200)
    montantJustification = models.FloatField()
    infosBeneficiaire = models.TextField()


class Utilisateur(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField()
    motdepasse = models.PasswordField()

class Role(models.Model):
    pass

class Donateur(Utilisateur):
    pass

class Organisation(Utilisateur):
    nomOrganisation = models.CharField(max_length=100)
