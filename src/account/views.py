from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile

# Paquets necessaire pour l'envoi de mail
# Import pour l'envoi de l'email afin d'activer le nouveau compte
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model

# Import du fichier tokens.py/class AccountActivationTokenGenerator
from .tokens import account_activation_token

from cart.cart import Cart



# Create your views here.
@login_required
def dashboard(request):
	# Tableau de bord de l'utilisateur
	return render(request, 'account/dashboard.html')


def login_user(request):
	# Fonction de login utilisateur
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ("Vous êtes connecté ..."))
			cart = Cart(request)
			if not cart:
				return redirect('home')
			else:
				return redirect("cart_detail")
		else:
			messages.error(request, ("Il y a eu une erreur avec le login ou mot de passe ...  merci de recommencer ..."))
			return redirect('login')

	else:
		return render(request, 'account/login.html')



@login_required
def logout_user(request):
	# Fonction de logout avec redirection
	logout(request)
	messages.success(request, ("Vous êtes déconnecté... Merci de votre visite..."))
	return redirect('home')



def register(request):
	# Fonction pour la création d'un nouveau compte utilsateur
	if request.method == "POST":
		user_form = UserRegistrationForm(request.POST)
		
		if user_form.is_valid():
			# Création d'un objet utilisateur en attente
			new_user = user_form.save(commit=False)

			# On récupère le username et password pour se connecter automatiquement après 
			# l'inscription
			# username = user_form.cleaned_data['username']
			# password = user_form.cleaned_data['password']
			# Applique le nouveau mot de passe
			new_user.set_password(
				user_form.cleaned_data['password'])
			# Desactivation du nouvel utilisateur
			new_user.is_active = False
			# Sauvegarde du nouvel état de l'utilisateur
			new_user.save()

			# Fonction pour envoyer le mail de création du compte
			# en attente de la validation
			activateEmail(request, new_user, user_form.cleaned_data.get('username'))

			# Création de l'objet Profile
			Profile.objects.create(user=new_user)

			# On connecte le nouvel utilisateur
			# user = authenticate(username=username, password=password)

			# login(request, user)
            
			# messages.success(request, 'Votre compte a été crée avec succes. Merci de bien vouloir compléter votre profil ...')
			return redirect('home')
        
		else:
			for error in list(user_form.errors.values()):
				messages.error(request, error)
			
			return redirect("register")
				
	else:
		user_form = UserRegistrationForm()
        
	return render(request, "account/register.html", {"user_form": user_form})


# Formulaire de modification du user et profile
@login_required
def edit(request):
	if request.method == "POST":
		# Modif 'first_name', 'last_name', 'email'
		user_form = UserEditForm(instance=request.user, data=request.POST)

		# Modif genre, date_of_birth, address_primary, postal_code_primary, city_primary,
		# phoneNumber1, phoneNumber2, address_secondery, postal_code_secondery, city_secondery
		profile_form = ProfileEditForm(
			instance=request.user.profile, data=request.POST, files=request.FILES
		)

		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, "Vos informations ont été sauvegardées avec succes ...")
			return redirect('home')
		
		else:
			messages.error(request, 'Un problème est survenu, vos données n\'ont pas été enregistrées.\
				  Merci de vérifier vos données dans le formulaire ...')
			return redirect('edit')
    
	else:
		user_form = UserEditForm(instance=request.user)
		profile_form = ProfileEditForm(instance=request.user.profile)

	context = {
		"user_form": user_form,
		"profile_form": profile_form,
		}

	return render(request, "account/edit.html", context)



def activateEmail(request, user, to_email):
	# Fonction pour l'envoi d'un mail lors de l'inscription
    mail_subject = 'Activer votre compte.'
    message = render_to_string('account/activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http',
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Bonjour {user}, Merci d\'accéder a votre mail et cliquer \
            sur le lien d\'activation que vous avez reçu. Note: N\'oubliez pas le dossier SPAM.')
    else:
        messages.error(request, f'Probleme pour envoyer le mail a  {to_email}, Vérifiez que l\'adresse saisie est correcte.')


def activate(request, uidb64, token):
	# Fonction attente retour clic sur mail d'activation nouveau compte
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Votre compte est activé. vous pouvez maintenant vous connecter et compléter votre Profil dans "Compte"')
        return redirect('login')
	
    else:
        messages.error(request, 'Le lien d\'activation est invalide')

    return redirect('home')