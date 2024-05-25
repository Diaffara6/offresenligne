from django.urls import path
from . import views



urlpatterns = [
    path("", views.connexion, name='Aconnexion'),
    path("deconnexion", views.deconnexion, name='Adeconnexion'),
    path("accueil/", views.accueil, name='accueil'),
    path("offres/", views.candidatures, name='candidatures'),
    path("accepter_offre/<str:id>", views.accepter_candidature, name='accepter_candidature'),
    path("refuser_offre/<str:id>", views.refuser_candidature, name='refuser_candidature'),
    path("entreprises/", views.entreprises, name='entreprises'),
    path("marche_public/", views.offres, name='offres'),
    path("ajouter_marche_public/", views.ajouter_offre, name='ajouter_offre'),
    path("modifier_marche_public/<str:code>/", views.modifier_offre, name='modifier_offre'),
    path("supprimer_marche_public/<str:code>/", views.supprimer_offre, name='supprimer_offre'),
    path("ajouter_employe/", views.ajouter_employeur, name='ajouter_employeur'),
    path("employes/", views.employeurs, name='employeurs'),
    path("modifier_employe/<int:id>/", views.modifier_employeur, name='modifier_employeur'),
    path("delete_employe/<int:id>/", views.delete_employeur, name='delete_employeur'),
    path("active_employe/<int:id>/", views.active_employeur, name='active_employeur'),
    path("offre_par_marche_public/<str:code>/", views.candidature_par_offre, name='candidature_par_offre'),
    path("affecte_employe_marche_public/<str:id>/", views.affecte_employe_marche_public, name='affecte_employe_marche_public'),
    path("ajouter_admin", views.ajouter_admin, name="ajouter_admin"),
    path("admins", views.admins, name="admins"),
    path("modifier_admin/<int:id>/", views.modifier_admin, name='modifier_admin'),
    path("delete_admin/<int:id>/", views.delete_admin, name='delete_admin'),
    path("active_admin/<int:id>/", views.active_admin, name='active_admin'),
    path("recherche", views.recherche, name='rechercher'),
    
] 