from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from param_blog import settings
from param_blog.settings import BASE_URL
from .models import *
from .models import Candidature
from django.contrib import messages
from datetime import datetime, date, time
from app_employeur.models import Employeur
from django.core.mail import send_mail
from django.utils.html import format_html
from html.parser import HTMLParser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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


# Function to send email
def send_email(sujet, contenue, destinataire:list):
    subject = sujet
    from_email = settings.EMAIL_HOST_USER
    to_email = destinataire

    validator = HTMLValidator()
    if validator.validate(contenue):
        try:
            send_mail(
                subject,
                '',
                from_email,
                to_email,
                html_message=contenue
            )
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'email : {e}")
    else:
        print("Contenu HTML invalide")


def inscription(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        if nom and prenom and email and password and password1:
            if '@' not in email:
                messages.error(request, "type d'email incorrect" )
            elif User.objects.filter(email=email).exists():
                messages.error(request, "cette adresse email a deja été utilisée ")
            elif password != password1:
                messages.error(request, "vos mots de passes ne correspondent pas ")
            elif len(password) < 6:
                messages.error(request, "votre mot de passe doit avoir au moins 6 caracteres ")
            else:
                user = User.objects.create_user(username=email, first_name=prenom, last_name=nom, email=email, password=password)
                if user:
                    login(request,user=user)
                    try:
                        Entreprise.objects.get(utilisateur=user)
                        return redirect('index')
                    except:
                        return redirect('entreprise')

        else:
            messages.error(request, 'vous devez remplir tous les champs ')
    try:
        context={'nom': nom, 'prenom': prenom, 'email': email}
    except:
        context = {}
    return render(request=request, template_name='blog/inscription.html', context=context)


@login_required(login_url='connexion')
def entreprise(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            nom_entrep = request.POST.get('nom_entrep')
            adresse_entrep = request.POST.get('adresse_entrep')
            email = request.POST.get('email')
            activite = request.POST.get('activite')
            idtel = request.POST.get('idtel')
            secteur = request.POST.get('secteur')
            telephone = request.POST.get('telephone')
            immatriculation = request.POST.get('immatriculation')
            if nom_entrep and adresse_entrep and email and telephone and idtel:
                if '@' not in email:
                    messages.error(request, "adresse email incorrect")
                elif Entreprise.objects.filter(nom_entrep=nom_entrep).exists():
                    messages.error(request, "cette entreprise a deja été enregistrée ")
                elif Entreprise.objects.filter(email_entrep=email).exists():
                    messages.error(request, "cette adresse email a deja été utilisée ")
                elif not telephone.isdigit():
                    messages.error(request, "le téléphone ne doit contenir que des entiers")
                elif not idtel:
                    messages.error(request, "choisissez l'id de votre pays")
                elif not activite and not secteur:
                    messages.error(request, "Ajoutez votre secteur d'activité")
                else:
                    try:
                        Entreprise.objects.get(utilisateur=request.user)
                        messages.error(request, "vous avez deja ajouté une entreprise")
                    except:
                        e = Entreprise.objects.create(utilisateur=request.user, nom_entrep=nom_entrep,
                                                adresse_entrep=adresse_entrep, email_entrep=email,idtel=idtel,
                                                telephone=telephone)
                        if immatriculation:
                            e.immatriculation = immatriculation
                            e.save()
                        if activite and activite != 'autre':
                            e.activite = activite
                            e.save()
                        if secteur:
                            e.secteur = secteur
                            e.save()
                        messages.success(request, "vos informations ont été ajoutées avec succès")

                        message = format_html("""
                            <span style="color: black;">Bonjour/Bonsoir {} {},<br><br>
                            Félicitations, le compte de votre entreprise a été créé avec succès !<br><br>
                            Nom de l'entreprise : {}<br>
                            Adresse : {}<br>
                            Téléphone : {}<br><br>
                            Merci de nous avoir choisis.<br><br>
                            Cordialement,<br>
                            L'équipe d'ENABEL-GUINEE
                            {}
                            </span>
                        """, request.user.first_name,request.user.last_name, nom_entrep, adresse_entrep, telephone, BASE_URL)

                        send_email(sujet='Création de compte réussie', contenue=message, destinataire=[email,request.user.email])
                        return redirect('index')
            else:
                messages.error(request, "tous les champs doivent etre remplit")
        try:
            context = {'nom_entrep': nom_entrep, 'adresse_entrep': adresse_entrep,
                            'email': email, 'activite': activite, 'telephone': telephone}
        except:
            context = {}
    return render(request=request, template_name='blog/entreprise.html', context=context)



def connexion(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password:
            user = authenticate(username=email, password=password)
            if user:
                login(request, user=user)
                if user.is_superuser or Employeur.objects.filter(utilisateur=user).exists():
                    return redirect('index')
                try:
                    Entreprise.objects.get(utilisateur=user)
                    return redirect('index')
                except:
                    return redirect('entreprise')
            else:
                messages.error(request, "l'email ou le mot de passe est incorrect")
    try:
        context = {'email': email}
    except:
        context = {}
    return render(request=request, template_name='blog/connexion.html', context=context)

@login_required(login_url='connexion')
def deconnexion(request):
    logout(request=request)
    messages.error(request, "Vous avez été deconnecté(e)")
    return redirect('index')


def compare_date_heure(offre):
    aujourd_hui = date.today()
    maintenant = datetime.now().time()

    if offre.date_limite < aujourd_hui:
        return False
    elif offre.date_limite == aujourd_hui and offre.heure_limite <= maintenant:
        return False
    else:
        return True




def index(request):
    page = request.GET.get('page', 1)
    paginator = Paginator(Marche_public.objects.all().order_by('-date_pub'), 10)  # Afficher 10 offres par page

    try:
        offres = paginator.page(page)
    except PageNotAnInteger:
        offres = paginator.page(1)
    except EmptyPage:
        offres = paginator.page(paginator.num_pages)

    for offre in offres:
        offre.status = compare_date_heure(offre)
        offre.save()

    context = {'offres': offres}
    return render(request=request, template_name='blog2/index.html', context=context)

def guide(request):
    return render(request=request, template_name='blog/guide.html')



def detail(request, id):
    offre = get_object_or_404(Marche_public, pk=id)
    context = {'offre': offre}
    return render(request=request, template_name='blog/detail.html', context=context)



def postuler(request, id):
    if request.user.is_authenticated:
        offre = get_object_or_404(Marche_public, pk=id)

        if not offre.status:
            messages.error(request, "La date limite pour postuler à ce marché public est dépassée.")
            return redirect('index')
        if request.user.is_superuser or Employeur.objects.filter(utilisateur=request.user).exists():
            messages.error(request, "Désolé vous n'avez pas le droit de postuler")
            return redirect('index')

        try:
            entreprise = Entreprise.objects.get(utilisateur=request.user)
        except Entreprise.DoesNotExist:
            return redirect('entreprise')

        if request.method == "POST":
            fichiers_proposition = [
                request.FILES.get(f'proposition{i}') for i in range(1, 6)
            ]

            proposition_fields = [
                'proposition1', 'proposition2', 'proposition3', 'proposition4', 'proposition5'
            ]

            try:
                Candidature.objects.get(offre=offre, entreprise=entreprise)
                messages.error(request, "Vous avez déjà postulé pour ce marché public.")
            except Candidature.DoesNotExist:
                candidature = Candidature(offre=offre, entreprise=entreprise)

                for i, fichier in enumerate(fichiers_proposition):
                    if i == 0 and not fichier:
                        messages.error(request, "Veuillez insérer un fichier dans le premier champ.")
                        return redirect(request.META.get('HTTP_REFERER'))

                    elif fichier:
                        if fichier.name.endswith('.pdf'):
                            setattr(candidature, proposition_fields[i], fichier)
                        else:
                            messages.error(request, f"Format de fichier incorrect (pdf uniquement)  pour le fichier {i + 1}.")
                            return redirect(request.META.get('HTTP_REFERER'))

                candidature.save()
                messages.success(request, "Vous avez postulé avec succès.")
                message = format_html("""
                    <span style="color: black;">Bonjour/Bonsoir {} {},<br><br>
                    Félicitations, vous avez postulé avec succès au marché public suivant : {}!<br><br>
                    Veuillez cliquer sur le lien suivant pour voir l'etat de votre candidature :<br>
                    {}/ma_candidature

                    Merci de nous avoir choisis.<br><br>
                    Cordialement,<br>
                    L'équipe d'ENABEL-GUINEE
                    {}
                    </span>
                """, request.user.first_name, request.user.last_name, offre.code, BASE_URL,BASE_URL)

                send_email(sujet=f'Confirmation de votre candidature pour le marché public ({offre.code})', contenue=message, destinataire=[entreprise.email_entrep,request.user.email])
                return redirect(to='index')

        context = {'offre': offre}
    else:
        context = {'message': 'Veuillez vous connecter pour pouvoir postuler.'}

    return render(request=request, template_name='blog/postuler.html', context=context)


def ma_candidature(request):
    if request.user.is_authenticated:  # Vérifie si l'utilisateur est connecté
        try:
            entreprise = get_object_or_404(Entreprise,utilisateur=request.user)
            historique = Candidature.objects.filter(entreprise=entreprise)
            context = {'historique': historique}
        except:
            context={}


    else:
        context = {'message': "Veuillez vous connecter pour voir l'état de votre candidature."}
    return render(request=request, template_name='blog/candidature.html', context=context)


def apropos(request):
    return render(request, "blog2/apropos.html")
