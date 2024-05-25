from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Employeur
from django.contrib.auth.decorators import login_required
from app_blog.models import Marche_public, Candidature
from datetime import datetime, date, time


def connexion(request):
    if request.user.is_authenticated and Employeur.objects.filter(utilisateur=request.user).exists():
        return redirect('debut')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                employeur = Employeur.objects.filter(utilisateur=user).exists()
                if employeur:
                    login(request, user)
                    return redirect('debut')  # Rediriger vers la page d'accueil des employeurs
                else:
                    messages.error(request, "Vous n'êtes pas autorisé à vous connecter en tant qu'employé.")
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
    return render(request, 'employe/connexion.html')



def deconnexion(request):
    logout(request=request)
    messages.success(request, "Vous avez été déconnecté(e)")
    return redirect('Empconnexion')

def compare_date_heure(marche):
    aujourd_hui = date.today()
    maintenant = datetime.now().time()

    if marche.date_limite < aujourd_hui:
        return False
    elif marche.date_limite == aujourd_hui and marche.heure_limite <= maintenant:
        return False
    else:
        return True
    

def _changement_template(request, template_name):
    aujourd_hui = date.today()
    
    offres = Marche_public.objects.filter(employe=request.user)
    for offre in offres:
        offre.status = compare_date_heure(offre)
        offre.save()
        offre.nombre_candidatures = Candidature.objects.filter(offre=offre).count()
    
    if request.method == 'POST':
        code1 = request.POST.get("code1")
        code2 = request.POST.get("code2")
        offre_code = request.POST.get("offre_code")
        if code1 and code2:
            try:
                Employeur.objects.get(utilisateur=request.user, code1=code1, code2=code2)
                messages.success(request, "Déverrouillage effectué avec succès")
                return redirect(f"offre_par_marche_public/{offre_code}")
            except Employeur.DoesNotExist:
                messages.error(request, "Déverrouillage échoué")
        else:
            messages.error(request, "Les deux champs doivent être remplis")
    
    context = {"offres": offres, 'today': aujourd_hui}
    return render(request, template_name, context=context)

    
@login_required(login_url='Empconnexion')
def debut(request):
    return _changement_template(request, 'employe/debut.html')


@login_required(login_url='Empconnexion')
def historique(request):
    return _changement_template(request, 'employe/historique.html')




@login_required(login_url='Empconnexion')
def offre_par_marche_public(request, code):
    aujourd_hui = date.today()
    offre = get_object_or_404(Marche_public, pk=code)
    candidatures = Candidature.objects.filter(offre=offre).select_related('entreprise')
    
    context = {
        "offre": offre,
        "candidatures": candidatures,
        "today": aujourd_hui,
    }
    return render(request, template_name="employe/offres.html", context=context)


@login_required(login_url='Empconnexion')
def accepter_candidature(request,id):
    candidature = get_object_or_404(Candidature, pk=id)
    if not candidature.retenu:
        candidature.retenu = True
        candidature.refuser = False 
        candidature.save()
        messages.success(request, f"{candidature.entreprise.nom_entrep} a été acceptée avec succes ")
    return redirect(request.META.get('HTTP_REFERER'))



@login_required(login_url='Empconnexion')
def refuser_candidature(request,id):
    candidature = get_object_or_404(Candidature, pk=id)
    if not candidature.refuser:
        candidature.retenu = False
        candidature.refuser = True 
        candidature.save()
        messages.success(request, f"{candidature.entreprise.nom_entrep} a été refusée avec succes ")
    return redirect(request.META.get('HTTP_REFERER'))
