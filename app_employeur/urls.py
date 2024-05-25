from django.urls import path
from .views import *
urlpatterns = [
path('',connexion, name='Empconnexion'),
path('deconnexion',deconnexion, name='Empdeconnexion'),
path('accueil',debut, name='debut'),
path('historique',historique, name='historique'),
path('offre_par_marche_public/<str:code>',offre_par_marche_public, name='offre_par_mp'),
path('accepter_candidature/<str:id>',accepter_candidature, name='accepter'),
path('refuser_candidature/<str:id>',refuser_candidature, name='refuser'),

    
] 