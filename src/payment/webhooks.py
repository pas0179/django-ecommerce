"""
Permet de récupérer les infos sur le reglement par un client
avec l'api de stripe

"""
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from order.models import Order
from order.task import payment_completed


@csrf_exempt
def stripe_webhooks(request):

    payload = request.body.decode('utf-8')

    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET,
            )
        
    except ValueError as e:
        # payload invalid
        print(f'Erreur de parsing du payload {str(e)}')        
        return HttpResponse(status=400)
    
    except stripe.error.SignatureVerificationError as e:
        # Signature invalide 
        print(f'Erreur vérification signature {str(e)}')
        return HttpResponse(status=400)
    
    # Récup des évenements
    if event.type == 'checkout.session.completed':
        session = event.data.object
        # Si retour de l'api stripe en réglé
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                order = Order.objects.get(id=session.client_reference_id)

            except Order.DoesNotExist:
                return HttpResponse(status=404)
            
            
            # Modifie strip_id avec la valeur du payment stripe
            order.stripe_id = session.payment_intent            
            # Modifie paid_status en true, soit réglé
            order.paid_status = True
            # Sauvegarde de order dans la base
            order.save()
            # Lancement task pour envoyer la facture par mail
            payment_completed.delay(order.id)
    
    return HttpResponse(status=200)

