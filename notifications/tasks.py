from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from monitoramento.models import Alerta, Idoso

@shared_task
def enviar_alerta_email(alerta_id):
    try:
        alerta = Alerta.objects.get(id=alerta_id)
        idoso = alerta.idoso
        
        subject = f'🚨 Alerta: {idoso.nome} - {alerta.get_tipo_display()}'
        message = f'''
        Alerta de Saúde Detectado!
        
        Paciente: {idoso.nome}
        Tipo: {alerta.get_tipo_display()}
        Nível: {alerta.get_nivel_display()}
        Mensagem: {alerta.mensagem}
        Horário: {alerta.timestamp.strftime("%d/%m/%Y %H:%M:%S")}
        
        Acesse o sistema para mais detalhes.
        '''
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [idoso.email_responsavel],
            fail_silently=False,
        )
        
        alerta.notificacao_email = True
        alerta.save()
        
        return f'Email enviado para {idoso.email_responsavel}'
    except Exception as e:
        return f'Erro: {str(e)}'

@shared_task
def gerar_relatorio_diario():
    idosos = Idoso.objects.filter(ativo=True)
    data_inicio = timezone.now() - timedelta(days=1)
    
    relatorio = []
    for idoso in idosos:
        dados = DadoSaude.objects.filter(
            idoso=idoso,
            timestamp__gte=data_inicio
        )
        
        if dados.exists():
            media_fc = dados.filter(frequencia_cardiaca__isnull=False).aggregate(
                avg=models.Avg('frequencia_cardiaca')
            )
            
            alertas = Alerta.objects.filter(
                idoso=idoso,
                timestamp__gte=data_inicio,
                visualizado=False
            ).count()
            
            relatorio.append({
                'idoso': idoso.nome,
                'media_fc': media_fc['avg'],
                'alertas': alertas,
                'quedas': dados.filter(queda_detectada=True).count()
            })
    
    # Aqui você pode salvar no banco ou enviar email
    return f'Relatório gerado com {len(relatorio)} idosos'