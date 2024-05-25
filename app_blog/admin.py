from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'nom_entrep', 'adresse_entrep','email_entrep','idtel','telephone', 'secteur','activite', 'date')


@admin.register(Marche_public)
class OffreAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'status','pays','doc1','doc2', 'date_pub', 'date_limite')


@admin.register(Candidature)
class CandidatureAdmin(admin.ModelAdmin):
    list_display = ('offre', 'entreprise','proposition1','retenu','date')
    list_editable = ('retenu',)
    list_filter = ('offre', 'entreprise', 'retenu',)


