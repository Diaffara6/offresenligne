from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.

class Entreprise(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)
    nom_entrep = models.CharField(max_length=115, verbose_name="Nom de l'entreprise")
    adresse_entrep = models.CharField(max_length=200, verbose_name="adresse de l'entreprise")
    email_entrep = models.EmailField(verbose_name="email de l'entreprise")
    idtel = models.CharField(max_length=10, blank=True)
    telephone = models.CharField(max_length=10)
    activite = models.CharField(max_length=115, verbose_name="domaine d'activité", blank=True)
    secteur = models.CharField(max_length=120, verbose_name="domaine d'activité" ,blank=True)
    immatriculation = models.CharField(max_length=30, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom_entrep



class Marche_public(models.Model):
    code = models.CharField(max_length=300, verbose_name="code de l'offre", primary_key=True)
    description = models.TextField()
    status = models.BooleanField(default=True)
    pays = models.CharField(max_length=20, default="Burkina Faso")
    employe = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    doc1 = models.FileField(upload_to='file/', blank=True, null=True)
    doc2 = models.FileField(upload_to='file/', blank=True, null=True)
    doc3 = models.FileField(upload_to='file/', blank=True, null=True)
    doc4 = models.FileField(upload_to='file/', blank=True, null=True)
    doc5 = models.FileField(upload_to='file/', blank=True, null=True)
    date_pub = models.DateTimeField(auto_now_add=True)
    date_limite = models.DateField()
    heure_limite = models.TimeField(blank=True, null=True)
    delai = models.DateField(blank=True, null=True)


    def __str__(self):
        return self.code


class Candidature(models.Model):
    offre = models.ForeignKey(to='Marche_public', on_delete=models.CASCADE)
    entreprise = models.ForeignKey(to='Entreprise', on_delete=models.CASCADE)
    proposition1 = models.FileField(upload_to='documents/', blank=True, null=True)
    proposition2 = models.FileField(upload_to='documents/', blank=True, null=True)
    proposition3 = models.FileField(upload_to='documents/', blank=True, null=True)
    proposition4 = models.FileField(upload_to='documents/', blank=True, null=True)
    proposition5 = models.FileField(upload_to='documents/', blank=True, null=True)
    retenu = models.BooleanField(default=False)
    refuser = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.entreprise.nom_entrep
