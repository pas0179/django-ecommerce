from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from django.conf import settings
from io import BytesIO
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from django.contrib.auth.models import User
from account.models import Profile


@shared_task
def payment_completed(request, order_id):
    """
    Tache pour envoyer un mail avec facture quand le reglement est fait
    """
    # Récup de l'objet order
    order = Order.objects.get(id=order_id)

    # Récup de l'objet User
    user = User.objects.filter(username=order.user).values()
    user_id = user[0]["id"]
    email = user[0]["username"]
    
    # Récup de l'objet profile
    profile = Profile.objects.filter(user=user_id)

    # Création du mail a envoyer
    subject = f'Sanncha - Facture n°. {order.id}'
    message = 'Veuillez trouver ci-joint la facture de votre achat récent.'
    email = EmailMessage(subject,
                message,
                'admin@sanncha.fr',
                [email])
    
    # generer le PDF
    html = render_to_string('order/pdf.html', {'order': order, "user": user, "profile": profile})
    out = BytesIO()
    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(out, stylesheets=stylesheets, presentational_hints=True)

    # Joint le fichier pdf
    email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')

    # Envoi de l'email
    email.send()


@shared_task
def order_created(order_id, user, email):
    """
    Tache pour envoyer un email de notification quand une commande
    est créer avec succès
    """
    
    order = Order.objects.get(id=order_id)
    subject = f'Commande n°. {order.id}'
    message = f'Bonjour {user},\n\n' \
                        f'Vous avez commandé sur notre boutique.\n' \
                        f'Votre n° de commande est: {order.id}.\n'\
                        f'Total de votre commande: {order.total_order} €'
    mail_sent = send_mail(subject,
                        message,
                        'admin@sanncha.fr',
                        [email])
    return mail_sent