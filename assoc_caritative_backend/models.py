from django.db import models

# Create your models here.
class Utilisateur(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField()
    motdepasse = models.PasswordField()

class Cagnotte(models.Model):
    intituleCagnotte = models.CharField(max_length=200)
    montantCagnotte = models.FloatField()
    objectifMontantVise = models.FloatField()
    dateDebut = models.DateField()
    dateFin = models.DateField()
    utilisateur = models.ForeignKey(Utilisateur)


class Donateur(Utilisateur):
    pass

class Don(models.Model):
    intituleDon = models.CharField(max_length=200)
    montantDon = models.FloatField()
    utilisateur = models.ForeignKey(Utilisateur)
    donateur = models.ForeignKey(Donateur)
    cagnote = models.ForeignKey(Cagnotte)

class Organisation(Utilisateur):
    nomOrganisation = models.CharField(max_length=100)

class JustificationDon(models.Model):
    motif = models.CharField(max_length=200)
    montantJustification = models.FloatField()
    infosBeneficiaire = models.TextField()
    cagnotte = models.ForeignKey(Cagnotte)
    organisation = models.ForeignKey(Organisation)


class Role(models.Model):
    pass


