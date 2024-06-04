from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Employeur(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)
    fonction1 = models.CharField(max_length=40, blank=True)
    fonction2 = models.CharField(max_length=40, blank=True)
    email1 = models.CharField(max_length=100, blank=True)
    email2 = models.CharField(max_length=100, blank=True)
    code1 = models.CharField(max_length=16, blank=True)
    code2 = models.CharField(max_length=16, blank=True)
    active_offre = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.utilisateur.username