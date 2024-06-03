from django.urls import path
from .views import *
from django.contrib.auth import views

urlpatterns = [
    path('', index, name='index'),
    path('detail/<str:id>', detail, name='detail'),
    path('connexion', connexion, name='connexion'),
    path('entreprise', entreprise, name='entreprise'),
    path('deconnexion', deconnexion, name='deconnexion'),
    path('ma_candidature', ma_candidature, name='candidature'),
    path('inscription', inscription, name='inscription'),
    path('apropos', apropos, name='apropos'),
    path('guide', guide, name='guide'),
    path('postuler/<str:id>', postuler, name='postuler'),
    path('reset_password', views.PasswordResetView.as_view(template_name='blog/password_reset.html'),
         name='reset_password'),
    path('reset_password_send',
         views.PasswordResetDoneView.as_view(template_name='blog/password_reset_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>', views.PasswordResetConfirmView.as_view(template_name='blog'
                                                                                        '/password_reset_form.html'),
         name='password_reset_confirm'),
    path('reset_password_complete', views.PasswordResetCompleteView.as_view(template_name='blog'
                                                                                          '/password_reset_done.html'),
         name='password_reset_complete'),
    
]
