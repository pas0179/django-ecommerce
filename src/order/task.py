from celery import shared_task
from django.core.mail import send_mail
from .models import Order




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