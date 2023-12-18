from django.shortcuts import render, redirect
from django.contrib import messages

# Paquets necessaire pour l'envoi de mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .forms import ContactForm

# Create your views here.

def contact(request):

	form = ContactForm
	if request.method == "POST":
		form = ContactForm(request.POST)
		if form.is_valid():
			# On récuprère les données dans des variables
			first_name = form.cleaned_data["first_name"]
			last_name = form.cleaned_data['last_name']
			email = form.cleaned_data['email']
			phone = form.cleaned_data['phone']
			message = form.cleaned_data['message']

			# On essai d'envoyer le message par mail
			send_mail(request, first_name, last_name, email, phone, message)

			return redirect("home")
			
		else:
			messages.error(request, f'Erreur dans la saisie du formulaire de contact. Vérifier si tous les champs sont corrèctement renseignés')

	context = {
		'form': form,
	}

	return render(request, 'contact/contact.html', context)


# Fonction pour envoi d'un mail avec formatage du contenu
def send_mail(request, first_name, last_name, email, phone, message):
	mail_admin = "schpas0179@gmail.com"
	mail_subject = 'Contact.'
	message = render_to_string('contact/mail_contact.html', {
		'first_name': first_name,
        'last_name': last_name,
		'phone': phone,
		'email': email,
		'message': message,
        'protocol': 'https' if request.is_secure() else 'http',
    })

	email = EmailMessage(mail_subject, message, to=[mail_admin])
	if email.send():
		messages.success(request, f'Bonjour {first_name}, votre demande de contact a été envoyé')

	else:
		messages.error(request, f'Un problème est survenu et votre demande de contact n\'a pas été envoyé')
