from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .utils import SMS

@shared_task
def enviar_alerta_email(alerta_id, destinatario):
    try:
        from monitoramento.models import Alerta
        alerta = Alerta.objects.get(id=alerta_id)
        
        send_mail(
            subject=f'🚨 Alerta de Saúde: {alerta.idoso.nome}',
            message=alerta.mensagem,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[destinatario],
            fail_silently=False,
        )
        return 'Email enviado com sucesso'
    except Exception as e:
        return f'Erro ao enviar email: {str(e)}'

@shared_task
def enviar_alerta_sms(alerta_id, telefone):
    try:
        from monitoramento.models import Alerta
        alerta = Alerta.objects.get(id=alerta_id)
        
        sms = SMS()
        sms.enviar(telefone, f'Alerta {alerta.idoso.nome}: {alerta.mensagem[:100]}')
        return 'SMS enviado'
    except Exception as e:
        return f'Erro ao enviar SMS: {str(e)}'