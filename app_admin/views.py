import random
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from app_employeur.models import Employeur
from django.urls import reverse
from django.contrib import messages
from app_blog.models import *
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, date
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.utils.html import format_html
from html.parser import HTMLParser
from param_blog import settings
from param_blog.settings import BASE_URL
from django.contrib.auth.hashers import check_password
from django.utils import formats
import locale
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

class HTMLValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.valid = True

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass

    def validate(self, html):
        self.valid = True
        try:
            self.feed(html)
        except:
            self.valid = False
        return self.valid


def format_date(date_string):
    # Définir la localisation sur le français
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

    # Convertir la chaîne de caractères en objet datetime
    date = datetime.strptime(date_string, "%Y-%m-%d")

    # Formater la date selon le format spécifié
    formatted_date = date.strftime("%A le %d %B %Y")
    return formatted_date


def send_mail_to_employers(username, password, email, code1='', code2=''):
    info = f"""
------------
{code1}
-----------
Vous avez été designé comme le 1er employé """ if code1 else f"""
------------
{code2}
------------
Vous avez été designé comme le 2em employé"""
    message = f"""
Bonjour/Bonsoir,

Félicitations ! Vous avez été ajouté en tant qu'employé avec succès.

Voici les informations de connexion de votre groupe pour acceder à votre compte :

**********************************
Numero du Marché : {username}
Mot de passe : {password}
**********************************
Voici votre code de deverouillage :
{info}
NB: le code de deverouillage est confidentiel

{BASE_URL}/cellulemarchespublics_log

Cordialement,
L'équipe d'ENABEL-BURKINA FASO

    """
    validator = HTMLValidator()
    if validator.validate(message):
        try:
            send_mail(
                "Informations d'inscription en tant qu'employé",
                message,
                settings.EMAIL_HOST_USER,
                [email]
            )
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'email : {e}")
    else:
        print("Contenu HTML invalide")


def send_mail_to_employers_affectation(date, email, marche, code1='', code2=''):
    date = format_date(date)
    info = f"""{code1}
        Vous avez été designé comme le 1er employé """ if code1 else f"""{code2}
        Vous avez été designé comme le 2em employé"""
    message = f"""
    <html>
    <head></head>
    <body>
        <p>Bonjour/Bonsoir, </p>

        <p>Félicitations ! Le marché public dont la réference est : {marche} vous a été affecté pour son évaluation
        jusqu'au {date}</p>

        <p>Rappel : <p>
        <p>Voici votre code de déverrouillage :</p>
        ---------------------------------
        <p>{info}</p>
        ---------------------------------
        <p>NB: le code de déverrouillage est confidentiel</p>

         <p>{BASE_URL}/cellulemarchespublics_log</p>

        <p>Cordialement,<br>
        L'équipe d'ENABEL-BURKINA FASO</p>

    </body>
    </html>
    """

    try:
        send_mail(
            subject="Affectation à un marché public",
            message='',
            html_message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
        )

    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")



def send_mail_to_admin_affectation(nom,prenom,username,password,email):
    message = f"""
    <html>
    <head></head>
    <body>
        <p>Bonjour/Bonsoir, {nom} {prenom} </p>

        <p>Félicitations ! Vous avez été ajouté en tant qu'administrateur pour la gestion de notre plateforme.</p>

        <p>Voici vos informations de connexion : </p>
        ---------------------------------
        <p>Nom d'utilisateur : {username}</p>
        <p>Mot de passe : {password}</p>
        ---------------------------------
        <p>NB: Nous vous recommandons de changer votre mot de passe lors de votre première connexion pour des raisons de sécurité</p>
        <p>Pour accéder à l'interface administrateur, veuillez cliquer ici : {BASE_URL}/enabeladmin </p>
        <p>Si vous avez des questions ou rencontrez des difficultés, n'hésitez pas à nous contacter. </p>

        <p>Cordialement,<br>
        L'équipe d'ENABEL-BURKINA FASO</p>

    </body>
    </html>
    """

    try:
        send_mail(
            subject="Ajout en tant qu'Administrateur de la Plateforme d'ENABEL BURKINA",
            message='',
            html_message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
        )

    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")



def connexion(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        if request.method == "POST":
            email = request.POST['email']
            password = request.POST['password']
            if email and password:
                user = authenticate(username=email, password=password)
                if user and user.is_superuser:
                    login(request, user=user)
                    return redirect("accueil")
                else:
                    messages.error(request, "Vous n'êtes pas autorisé à vous connecter.")
            else:
                messages.error(request, "Veuillez fournir l'identifiant et le mot de passe.")
        return render(request=request, template_name="app_admin/index.html")
    return redirect("accueil")  # Redirigez si déjà connecté


def is_superuser(user):
    return user.is_superuser


@user_passes_test(is_superuser, login_url="Aconnexion")
def deconnexion(request):
    logout(request)
    messages.error(request, "Vous avez été déconnecté(e).")
    return redirect('Aconnexion')


def compare_date_heure(offre):
    aujourd_hui = date.today()
    maintenant = datetime.now().time()

    if offre.date_limite < aujourd_hui:
        return False
    elif offre.date_limite == aujourd_hui and offre.heure_limite <= maintenant:
        return False
    else:
        return True


@user_passes_test(is_superuser, login_url="Aconnexion")
def accueil(request):
    les_candidatures = Candidature.objects.all()
    les_entreprises = Entreprise.objects.all()
    entreprises = Entreprise.objects.all()[:3]
    les_offres = Marche_public.objects.all()
    if les_offres:
        for offre in les_offres:
            offre.status = compare_date_heure(offre)
            offre.save()
    les_employeurs = Employeur.objects.all()
    context = {"les_candidatures": les_candidatures, "les_entreprises": les_entreprises, "entreprises": entreprises,
               "les_offres": les_offres, "les_employeurs": les_employeurs}
    return render(request=request, template_name="app_admin/accueil.html", context=context)


@user_passes_test(is_superuser, login_url="Aconnexion")
def candidatures(request):

    offres = Marche_public.objects.all().order_by('-date_pub')
    if offres:
        for offre in offres:
            if offre.employe:
                employeur = Employeur.objects.get(utilisateur=offre.employe)
                if employeur.active_offre == offre.code:
                    offre.ouvert = True
                    offre.save()
            offre.nombre_candidatures = Candidature.objects.filter(offre=offre).count()
        page = request.GET.get('page', 1)
        paginator = Paginator(offres, 6)  # Afficher 6 marche publics
        try:
            offres = paginator.page(page)
        except PageNotAnInteger:
            offres = paginator.page(1)
        except EmptyPage:
            offres = paginator.page(paginator.num_pages)
    context = {"offres": offres}
    return render(request, template_name="app_admin/candidatures.html", context=context)


@user_passes_test(is_superuser, login_url="Aconnexion")
def candidature_par_offre(request, code):
    offre = get_object_or_404(Marche_public, pk=code)
    candidatures = Candidature.objects.filter(offre=offre).select_related('entreprise')

    context = {
        "offre": offre,
        "candidatures": candidatures,
    }
    return render(request, template_name="app_admin/detail_candidature.html", context=context)


@user_passes_test(is_superuser, login_url="Aconnexion")
def accepter_candidature(request, id):
    candidature = get_object_or_404(Candidature, pk=id)
    if not candidature.retenu:
        candidature.retenu = True
        candidature.refuser = False
        candidature.save()
        messages.success(request, f"{candidature.entreprise.nom_entrep} a été acceptée avec succes ")
    return redirect("candidatures")


@user_passes_test(is_superuser, login_url="Aconnexion")
def refuser_candidature(request, id):
    candidature = get_object_or_404(Candidature, pk=id)
    if not candidature.refuser:
        candidature.retenu = False
        candidature.refuser = True
        candidature.save()
        messages.success(request, f"{candidature.entreprise.nom_entrep} a été refusée avec succès ")
    return redirect("candidatures")


@user_passes_test(is_superuser, login_url="Aconnexion")
def affecte_employe_marche_public(request, id):
    offre = get_object_or_404(Marche_public, pk=id)
    employeurs = Employeur.objects.all().order_by('-pk')
    if request.method == "POST":
        employe = request.POST.get("employe")
        date_limite = request.POST.get("date_limite")

        if employe and date_limite:
            offre.employe = User.objects.get(username=employe)
            offre.delai = date_limite
            offre.save()
            employe = Employeur.objects.get(utilisateur=offre.employe)
            messages.success(request,
                             f"utilisateur ({offre.employe}) affecté avec succès au marché public ({offre.pk})")
            send_mail_to_employers_affectation(date=offre.delai, marche=offre.code, code1=employe.code1,
                                               email=employe.email1)
            send_mail_to_employers_affectation(date=offre.delai, code2=employe.code2, marche=offre.code,
                                               email=employe.email2)
            return redirect("candidatures")
        else:
            messages.error(request, "remplissez correctement tous les champs")
    context = {
        'offre': offre,
        'employeurs': employeurs,
    }
    return render(request, template_name="app_admin/modifier_candidature.html", context=context)


@user_passes_test(is_superuser, login_url="Aconnexion")
def entreprises(request):
    entreprises =  Entreprise.objects.all().order_by("-date")
    page = request.GET.get('page', 1)
    paginator = Paginator(entreprises, 10)  # Afficher 10 entreprises par page

    try:
        entreprises_paginated = paginator.page(page)
    except PageNotAnInteger:
        entreprises_paginated = paginator.page(1)
    except EmptyPage:
        entreprises_paginated = paginator.page(paginator.num_pages)

    context = {"entreprises": entreprises_paginated}
    return render(request, template_name="app_admin/entreprise.html", context=context)


@user_passes_test(is_superuser, login_url="Aconnexion")
def offres(request):
    offres = Marche_public.objects.all().order_by("-date_pub")
    if offres:
        for offre in offres:
            offre.status = compare_date_heure(offre)
            offre.save()
    page = request.GET.get('page', 1)
    paginator = Paginator(offres, 5)  # Afficher 6 marche publics
    try:
        offres = paginator.page(page)
    except PageNotAnInteger:
        offres = paginator.page(1)
    except EmptyPage:
        offres = paginator.page(paginator.num_pages)
    context = {"offres": offres,
               }
    return render(request, template_name="app_admin/offres.html", context=context)


@user_passes_test(is_superuser, login_url="Aconnexion")
def ajouter_offre(request):
    if request.method == "POST":
        code = request.POST['code']
        description = request.POST['description']
        pays = request.POST['pays']
        if not pays:
            pays = 'Burkina Faso'
        date_limite = request.POST['date_limite']
        heure_limite = request.POST['heure_limite']

        if code and date_limite and heure_limite:
            fichiers_doc = [
                request.FILES.get(f'doc{i}') for i in range(1, 6)
            ]

            doc_fields = [
                'doc1', 'doc2', 'doc3', 'doc4', 'doc5'
            ]

            if Marche_public.objects.filter(code=code).exists():
                messages.error(request, "ce code de marché existe deja .")
            else:
                offre = Marche_public(code=code, description=description, pays=pays, date_limite=date_limite,
                                      heure_limite=heure_limite)

                for i, fichier in enumerate(fichiers_doc):
                    if i == 0 and not fichier:
                        messages.error(request, "Veuillez insérer un fichier dans le premier champ.")
                        return redirect(request.META.get('HTTP_REFERER'))

                    elif fichier:
                        if fichier.name.endswith(('.docx', '.pdf')):
                            setattr(offre, doc_fields[i], fichier)
                        else:
                            messages.error(request,
                                           f"Format de fichier incorrect (pdf ou docx) pour le fichier {i + 1}.")
                            return redirect(request.META.get('HTTP_REFERER'))

                offre.save()
                messages.success(request, "Publication effectuée avec succes")
                return redirect("offres")
        else:
            messages.error(request, "aucun de ces trois(3) champs ne doit être vide (code, date limite et l'heure) ")

    return render(request, template_name="app_admin/ajouter_offre.html")


@user_passes_test(is_superuser, login_url="Aconnexion")
def modifier_offre(request, code):
    offre = get_object_or_404(Marche_public, code=code)

    if request.method == "POST":
        description = request.POST['description']
        pays = request.POST['pays']
        date_limite = request.POST['date_limite']
        heure_limite = request.POST['heure_limite']

        fichiers_doc = [
            request.FILES.get(f'doc{i}') for i in range(1, 6)
        ]

        doc_fields = [
            'doc1', 'doc2', 'doc3', 'doc4', 'doc5'
        ]

        for i, fichier in enumerate(fichiers_doc):
            if fichier:
                if fichier.name.endswith(('.docx', '.pdf')):
                    setattr(offre, doc_fields[i], fichier)
                else:
                    messages.error(request, f"Format de fichier incorrect (pdf ou docx) pour le fichier {i + 1}.")
                    return redirect(request.META.get('HTTP_REFERER'))
        if description:
            offre.description = description
        if date_limite:
            offre.date_limite = date_limite
        if heure_limite:
            offre.heure_limite = heure_limite
        if pays:
            offre.pays = pays
        offre.save()
        messages.success(request, f"Modification du marché public ({offre.code}) effectuée avec succès.")
        return redirect("offres")

    context = {'offre': offre}
    return render(request, template_name="app_admin/modifier_offre.html", context=context)


@user_passes_test(is_superuser, login_url="Aconnexion")
def supprimer_offre(request, code):
    offre = get_object_or_404(Marche_public, pk=code)
    messages.error(request, f"le marché public ({offre.code}) a été supprimé avec succès")
    offre.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@user_passes_test(is_superuser, login_url="Aconnexion")
def ajouter_employeur(request):
    username = ''
    fonction1 = ''
    fonction2 = ''
    email1 = ''
    email2 = ''
    nom1 = ''
    nom2 = ''
    password = ''
    password1 = ''
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        fonction1 = request.POST["fonction1"]
        fonction2 = request.POST["fonction2"]
        nom1 = request.POST["nom1"]
        nom2 = request.POST["nom2"]
        password = request.POST["password"]
        password1 = request.POST["password1"]
        code1 = ''.join(random.choices('0123456789', k=6))
        code2 = ''.join(random.choices('0123456789', k=6))
        email1 = request.POST["email1"]
        email2 = request.POST["email2"]
        if username and password and password1 and code1 and code2 and nom1 and nom2 and fonction1 and fonction2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "ce  Numero de marché existe deja pour un autre employé ")
            elif password != password1:
                messages.error(request, "vos mots de passes ne correspondent pas ")
            elif len(password) < 6:
                messages.error(request, "votre mot de passe doit avoir au moins 6 caracteres ")
            elif code1 == code2:
                messages.error(request, "Les deux codes ne doivent pas etre identiques")
            elif not email1 or not email2:
                messages.error(request, "Vous devez ajouter l'adresse email des employés")
            else:
                user = User.objects.create_user(username=username, password=password)
                Employeur.objects.create(utilisateur=user, fonction1=fonction1, fonction2=fonction2, code1=code1,
                                         code2=code2, nom1=nom1, nom2=nom2, email1=email1, email2=email2)
                if user:
                    messages.success(request, "Groupe d'employé ajouté avec succès ")
                    send_mail_to_employers(username=username, password=password, email=email1, code1=code1)
                    send_mail_to_employers(username=username, password=password, email=email2, code2=code2)
                    return redirect("employeurs")
        else:
            messages.error(request, "Remplissez correctement tous les champs")

        context = {'username': username,
                   'fonction1': fonction1,
                   'fonction2': fonction2,
                   'password': password,
                   'password1': password1,
                   'email1': email1,
                   'email2': email2,
                   'nom1': nom1,
                   'nom2': nom2,
                   }
    return render(request, template_name="app_admin/ajouter_employeur.html", context=context)


@user_passes_test(is_superuser, login_url="Aconnexion")
def modifier_employeur(request, id):
    user = get_object_or_404(User, pk=id)
    e = Employeur.objects.get(utilisateur=user)

    if request.method == "POST":
        username = request.POST.get("username")
        fonction1 = request.POST.get("fonction1")
        fonction2 = request.POST.get("fonction2")
        nom1 = request.POST.get("nom1")
        nom2 = request.POST.get("nom2")
        password = request.POST.get("password")
        password1 = request.POST.get("password1")
        email1 = request.POST["email1"]
        email2 = request.POST["email2"]
        code1 = ''.join(random.choices('0123456789', k=6))
        code2 = ''.join(random.choices('0123456789', k=6))

        if username == user.username or not User.objects.filter(username=username).exists():
            user.username = username
            user.save()
        else:
            messages.error(request, "cet Numero de marché existe deja pour un employé .")
            return redirect(request.META.get('HTTP_REFERER'))

        if password and password1:
            if password != password1:
                messages.error(request, "Vos mots de passe ne correspondent pas.")
                return redirect(request.META.get('HTTP_REFERER'))
            elif len(password) < 6:
                messages.error(request, "Le mot de passe doit avoir au moins 6 caractères.")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                hashed_password = make_password(password)
                user.password = hashed_password
                user.save()
        else:
            messages.error(request, "Ajouter un mot de passe.")
            return redirect(request.META.get('HTTP_REFERER'))



        if fonction1:
            e.fonction1 = fonction1
            e.save()
        if fonction2:
            e.fonction2 = fonction2
            e.save()
        if email1:
            e.email1 = email1
            e.save()
        if email2:
            e.email2 = email2
            e.save()
        if code1:
            e.code1 = code1
            e.save()
        if code2:
            e.code2 = code2
            e.save()
        if nom2:
            e.nom2 = nom2
            e.save()
        if nom1:
            e.nom1 = nom1
            e.save()

        messages.error(request, "modification effectuée avec succès.")
        send_mail_to_employers(username=e.utilisateur.username, password=password, email=email1 if email1 else e.email1, code1=code1)
        send_mail_to_employers(username=e.utilisateur.username, password=password, email=email2 if email2 else e.email2, code2=code2)
        return redirect("employeurs")

    context = {
        'modif': 'modification',
        'utilisateur': user,
        'e': e,
    }

    return render(request, template_name="app_admin/ajouter_employeur.html", context=context)


@user_passes_test(is_superuser, login_url="Aconnexion")
def employeurs(request):
    employeurs = Employeur.objects.all().order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(employeurs, 10)  # Afficher 10 employeurs par page
    try:
        employeurs = paginator.page(page)
    except PageNotAnInteger:
        employeurs = paginator.page(1)
    except EmptyPage:
        employeurs = paginator.page(paginator.num_pages)
    context = {"employeurs": employeurs}
    return render(request, template_name="app_admin/employeurs.html", context=context)


@user_passes_test(is_superuser, login_url="Aconnexion")
def delete_employeur(request, id):
    user = get_object_or_404(User, pk=id)
    user.is_active = False
    user.save()
    messages.error(request, "Désactivation effectuée avec succes ")
    return redirect(request.META.get('HTTP_REFERER'))


@user_passes_test(is_superuser, login_url="Aconnexion")
def active_employeur(request, id):
    user = get_object_or_404(User, pk=id)
    user.is_active = True
    user.save()
    messages.success(request, "Activation effectuée avec succes ")
    return redirect(request.META.get('HTTP_REFERER'))


### La gestion des administrateurs
def is_staff(user):
    return user.is_staff


@user_passes_test(is_superuser, login_url="Aconnexion")
def ajouter_admin(request):
    username = ''
    nom = ''
    prenom = ''
    equipe = False
    email = ''
    context = {}
    if request.method == "POST":
        username = request.POST.get("username")
        nom = request.POST.get("nom")
        equipe = request.POST.get("equipe")
        prenom = request.POST.get("prenom")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password1 = request.POST.get("password1")

        # Vérification de la présence de toutes les données nécessaires
        if username and nom and prenom and email and password and password1:
            # Vérification que le nom d'utilisateur et l'adresse e-mail ne sont pas déjà utilisés
            if User.objects.filter(username=username).exists():
                messages.error(request, "Ce nom d'utilisateur est déjà utilisé.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Cette adresse e-mail est déjà utilisée.")
            # Vérification que les mots de passe correspondent et sont suffisamment longs
            elif password != password1:
                messages.error(request, "Les mots de passe ne correspondent pas.")
            elif len(password) < 6:
                messages.error(request, "Le mot de passe doit avoir au moins 6 caractères.")
            else:
                # Création de l'utilisateur avec les permissions appropriées
                user = User.objects.create_user(username=username, first_name=prenom, last_name=nom, password=password,
                                                email=email, is_superuser=True)
                if equipe:
                    user.is_staff = True
                    user.save()
                else:
                    user.is_staff = False
                    user.save()
                if user:
                    send_mail_to_admin_affectation(nom=nom,prenom=prenom,username=username,password=password,email=email)
                    messages.success(request, "Administrateur créé avec succès.")
                    return redirect("admins")
                else:
                    messages.error(request, "Une erreur est survenue lors de la création de l'administrateur.")
        else:
            messages.error(request, "Veuillez remplir correctement tous les champs.")

        context = {'username': username,
                   'nom': nom,
                   'prenom': prenom,
                   'email': email,
                   'equipe': equipe,
                   }

    return render(request, template_name="app_admin/admin.html", context=context)


@user_passes_test(is_superuser, login_url="Aconnexion")
def admins(request):
    admins = User.objects.filter(is_superuser=True).order_by('-date_joined')
    page = request.GET.get('page', 1)
    paginator = Paginator(admins, 10)  # Afficher 10 employeurs par page
    try:
        admins = paginator.page(page)
    except PageNotAnInteger:
        admins = paginator.page(1)
    except EmptyPage:
        admins = paginator.page(paginator.num_pages)
    context = {"admins": admins}
    return render(request, template_name="app_admin/admins.html", context=context)


@user_passes_test(is_superuser, login_url="Aconnexion")
def modifier_admin(request, id):
    user = get_object_or_404(User, pk=id)
    if not request.user.is_staff and user != request.user:
        return redirect('accueil')
    if request.method == "POST":
        nom = request.POST.get("nom")
        equipe = request.POST.get("equipe")
        prenom = request.POST.get("prenom")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password1 = request.POST.get("password1")

        if nom:
            user.last_name = nom
            user.save()
        if prenom:
            user.first_name = prenom
            user.save()
        if equipe:
            user.is_staff = True
            user.save()
        else:
            user.is_staff = False
            user.save()
        if email:
            user.email = email
            user.save()
        if password and password1:
            if password != password1:
                messages.error(request, "vos mots de passes ne correspondent pas ")
                return redirect(request.META.get('HTTP_REFERER'))
            elif len(password) < 6:
                messages.error(request, "votre mot de passe doit avoir au moins 6 caracteres ")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                hashed_password = make_password(password)
                user.password = hashed_password
                user.save()


        if request.user == user:
            messages.success(request, "Vos informations on été modifiées avec succès")
            login(request, user=user)
            return redirect('Aconnexion')
        if request.user.is_staff:
            messages.success(request, "modification effectuée avec succès ")
            return redirect("admins")
        else:
            messages.success(request, "modification effectuée avec succès ")
            return redirect("accueil")
    context = {
        'utilisateur': user,
        'modif': 'modification',
    }
    return render(request, template_name="app_admin/admin.html", context=context)


@user_passes_test(is_superuser, login_url="Aconnexion")
def delete_admin(request, id):
    user = get_object_or_404(User, pk=id)
    user.is_active = False
    user.save()
    messages.success(request, "Désactivation effectuée avec succès ")
    return redirect(request.META.get('HTTP_REFERER'))


@user_passes_test(is_superuser, login_url="Aconnexion")
def active_admin(request, id):
    user = get_object_or_404(User, pk=id)
    user.is_active = True
    user.save()
    messages.success(request, "Activation effectuée avec succes ")
    return redirect(request.META.get('HTTP_REFERER'))


@user_passes_test(is_superuser, login_url="Aconnexion")
def recherche(request):
    context = {}
    query = request.GET.get('q')

    if not query or query.isspace():
        messages.error(request, "Renseignez quelque chose dans la barre de recherche")
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        offres = Marche_public.objects.filter(code__icontains=query)
        for offre in offres:
            offre.status = compare_date_heure(offre)
            offre.save()
            offre.nombre_candidatures = Candidature.objects.filter(offre=offre).count()

        context = {
            'entrep': Entreprise.objects.filter(nom_entrep__icontains=query),
            'marche': offres,
            'employeurs': Employeur.objects.filter(utilisateur__username__icontains=query),
            'admins': User.objects.filter(is_superuser=True, username__icontains=query),
            'query': query,
        }

    return render(request, template_name="app_admin/recherche.html", context=context)