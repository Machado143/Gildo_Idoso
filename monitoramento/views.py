from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.db.models import Avg, Count, Min, Max  # Importações para agregações
from .models import Idoso, Dispositivo, DadoSaude, Alerta, HistoricoSaude
from .forms import IdosoForm, DispositivoForm
import csv
from django.http import HttpResponse

# Imports para PDF
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.enums import TA_CENTER

@require_http_methods(["GET", "POST"])
def public_add_idoso(request):
    """View pública para registro de idoso (requer aprovação)"""
    if request.method == 'POST':
        form = IdosoForm(request.POST)
        if form.is_valid():
            idoso = form.save(commit=False)
            idoso.ativo = False  # Requer aprovação do admin
            idoso.save()
            messages.success(request, '✅ Registro enviado! Entraremos em contato para aprovação.')
            return redirect('index')
    else:
        form = IdosoForm()
    
    return render(request, 'monitoramento/registrar_idoso_publico.html', {'form': form})

# ====================================================================================
# VIEWS PRINCIPAIS
# ====================================================================================

@login_required
def dashboard(request):
    """Dashboard principal com dados para gráficos"""
    idosos = Idoso.objects.filter(ativo=True)
    
    # Estatísticas gerais
    total_idosos = idosos.count()
    dispositivos_ativos = Dispositivo.objects.filter(ativo=True).count()
    alertas_recentes = Alerta.objects.filter(visualizado=False).count()
    
    # Últimos dados de saúde
    ultimos_dados = DadoSaude.objects.select_related('idoso').order_by('-timestamp')[:10]
    
    # Alertas não visualizados
    alertas_pendentes = Alerta.objects.filter(visualizado=False).order_by('-timestamp')[:5]
    
    # DADOS PARA GRÁFICOS - Últimas 24 horas
    vinte_quatro_horas_ago = timezone.now() - timedelta(hours=24)
    
    # Dados de Frequência Cardíaca (última 24h, agrupados de 4 em 4 horas)
    dados_fc = []
    labels_fc = []
    for i in range(6, 0, -1):
        inicio = timezone.now() - timedelta(hours=i*4)
        fim = timezone.now() - timedelta(hours=(i-1)*4)
        media = DadoSaude.objects.filter(
            timestamp__gte=inicio,
            timestamp__lt=fim,
            frequencia_cardiaca__isnull=False
        ).aggregate(Avg('frequencia_cardiaca'))['frequencia_cardiaca__avg']
        
        dados_fc.append(round(media) if media else 0)
        labels_fc.append(inicio.strftime('%Hh'))
    
    # Dados de Pressão Arterial
    dados_sistolica = []
    dados_diastolica = []
    for i in range(6, 0, -1):
        inicio = timezone.now() - timedelta(hours=i*4)
        fim = timezone.now() - timedelta(hours=(i-1)*4)
        
        media_sistolica = DadoSaude.objects.filter(
            timestamp__gte=inicio,
            timestamp__lt=fim,
            pressao_sistolica__isnull=False
        ).aggregate(Avg('pressao_sistolica'))['pressao_sistolica__avg']
        
        media_diastolica = DadoSaude.objects.filter(
            timestamp__gte=inicio,
            timestamp__lt=fim,
            pressao_diastolica__isnull=False
        ).aggregate(Avg('pressao_diastolica'))['pressao_diastolica__avg']
        
        dados_sistolica.append(round(media_sistolica) if media_sistolica else 0)
        dados_diastolica.append(round(media_diastolica) if media_diastolica else 0)
    
    # Distribuição de Alertas por Tipo
    alertas_por_tipo = Alerta.objects.values('tipo').annotate(
        total=Count('id')
    ).order_by('-total')[:5]
    
    labels_alertas = [a['tipo'].replace('_', ' ').title() for a in alertas_por_tipo]
    dados_alertas = [a['total'] for a in alertas_por_tipo]
    
    # Atividade Física (Passos) - Últimos 7 dias
    labels_passos = []
    dados_passos = []
    for i in range(6, -1, -1):
        dia = timezone.now() - timedelta(days=i)
        inicio_dia = dia.replace(hour=0, minute=0, second=0)
        fim_dia = dia.replace(hour=23, minute=59, second=59)
        
        total_passos = DadoSaude.objects.filter(
            timestamp__gte=inicio_dia,
            timestamp__lte=fim_dia,
            passos__isnull=False
        ).aggregate(Avg('passos'))['passos__avg']
        
        labels_passos.append(dia.strftime('%a'))
        dados_passos.append(round(total_passos) if total_passos else 0)
    
    context = {
        'idosos': idosos,
        'total_idosos': total_idosos,
        'dispositivos_ativos': dispositivos_ativos,
        'alertas_recentes': alertas_recentes,
        'ultimos_dados': ultimos_dados,
        'alertas_pendentes': alertas_pendentes,
        
        # Dados para gráficos
        'chart_labels_fc': labels_fc,
        'chart_dados_fc': dados_fc,
        'chart_labels_pressao': labels_fc,
        'chart_dados_sistolica': dados_sistolica,
        'chart_dados_diastolica': dados_diastolica,
        'chart_labels_alertas': labels_alertas,
        'chart_dados_alertas': dados_alertas,
        'chart_labels_passos': labels_passos,
        'chart_dados_passos': dados_passos,
    }
    return render(request, 'monitoramento/dashboard.html', context)

@login_required
def exportar_dados(request):
    """Exporta dados em CSV"""
    import csv
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="dados_idosos.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Nome', 'Data', 'Frequência', 'Pressão', 'Saturação', 'Temperatura', 'Passos', 'Queda', 'Emergência'])
    
    dados = DadoSaude.objects.select_related('idoso').order_by('-timestamp')[:10000]
    
    for dado in dados:
        writer.writerow([
            dado.idoso.nome,
            dado.timestamp.strftime('%d/%m/%Y %H:%M'),
            dado.frequencia_cardiaca or '',
            dado.pressao_arterial or '',
            dado.saturacao_oxigenio or '',
            dado.temperatura or '',
            dado.passos or '',
            'Sim' if dado.queda_detectada else 'Não',
            'Sim' if dado.botao_emergencia else 'Não'
        ])
    
    return response

def index(request):
    """Página inicial pública"""
    return render(request, 'monitoramento/index.html')

# ====================================================================================
# API ENDPOINTS PARA GRÁFICOS
# ====================================================================================

@login_required
def api_grafico_frequencia(request):
    """API para dados do gráfico de frequência cardíaca"""
    vinte_quatro_horas_ago = timezone.now() - timedelta(hours=24)
    
    dados = []
    labels = []
    
    for i in range(6, 0, -1):
        inicio = timezone.now() - timedelta(hours=i*4)
        fim = timezone.now() - timedelta(hours=(i-1)*4)
        media = DadoSaude.objects.filter(
            timestamp__gte=inicio,
            timestamp__lt=fim,
            frequencia_cardiaca__isnull=False
        ).aggregate(Avg('frequencia_cardiaca'))['frequencia_cardiaca__avg']
        
        dados.append(round(media) if media else 0)
        labels.append(inicio.strftime('%Hh'))
    
    return JsonResponse({
        'labels': labels,
        'data': dados
    })

@login_required
def api_grafico_pressao(request):
    """API para dados do gráfico de pressão arterial"""
    dados_sistolica = []
    dados_diastolica = []
    labels = []
    
    for i in range(6, 0, -1):
        inicio = timezone.now() - timedelta(hours=i*4)
        fim = timezone.now() - timedelta(hours=(i-1)*4)
        
        media_sistolica = DadoSaude.objects.filter(
            timestamp__gte=inicio,
            timestamp__lt=fim,
            pressao_sistolica__isnull=False
        ).aggregate(Avg('pressao_sistolica'))['pressao_sistolica__avg']
        
        media_diastolica = DadoSaude.objects.filter(
            timestamp__gte=inicio,
            timestamp__lt=fim,
            pressao_diastolica__isnull=False
        ).aggregate(Avg('pressao_diastolica'))['pressao_diastolica__avg']
        
        dados_sistolica.append(round(media_sistolica) if media_sistolica else 0)
        dados_diastolica.append(round(media_diastolica) if media_diastolica else 0)
        labels.append(inicio.strftime('%Hh'))
    
    return JsonResponse({
        'labels': labels,
        'sistolica': dados_sistolica,
        'diastolica': dados_diastolica
    })

@login_required
def api_grafico_alertas(request):
    """API para dados do gráfico de alertas"""
    alertas_por_tipo = Alerta.objects.values('tipo').annotate(
        total=Count('id')
    ).order_by('-total')[:5]
    
    labels = [a['tipo'].replace('_', ' ').title() for a in alertas_por_tipo]
    dados = [a['total'] for a in alertas_por_tipo]
    
    return JsonResponse({
        'labels': labels,
        'data': dados
    })

@login_required
def api_grafico_passos(request):
    """API para dados do gráfico de passos"""
    labels = []
    dados = []
    
    for i in range(6, -1, -1):
        dia = timezone.now() - timedelta(days=i)
        inicio_dia = dia.replace(hour=0, minute=0, second=0)
        fim_dia = dia.replace(hour=23, minute=59, second=59)
        
        total_passos = DadoSaude.objects.filter(
            timestamp__gte=inicio_dia,
            timestamp__lte=fim_dia,
            passos__isnull=False
        ).aggregate(Avg('passos'))['passos__avg']
        
        labels.append(dia.strftime('%a'))
        dados.append(round(total_passos) if total_passos else 0)
    
    return JsonResponse({
        'labels': labels,
        'data': dados
    })

# ====================================================================================
# RELATÓRIOS PDF
# ====================================================================================

@login_required
def gerar_relatorio_pdf_idoso(request, idoso_id):
    """Gera relatório PDF individual de um idoso"""
    idoso = get_object_or_404(Idoso, id=idoso_id)
    
    # Criar o objeto BytesIO
    buffer = io.BytesIO()
    
    # Criar o PDF
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    # Container para elementos
    elementos = []
    
    # Estilos
    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#0066CC'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    subtitulo_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#004C99'),
        spaceAfter=12,
    )
    
    # Título
    elementos.append(Paragraph(f"Relatório de Monitoramento", titulo_style))
    elementos.append(Paragraph(f"{idoso.nome}", titulo_style))
    elementos.append(Spacer(1, 12))
    
    # Data do relatório
    data_atual = datetime.now().strftime("%d/%m/%Y às %H:%M")
    elementos.append(Paragraph(f"<i>Gerado em: {data_atual}</i>", styles['Normal']))
    elementos.append(Spacer(1, 20))
    
    # INFORMAÇÕES PESSOAIS
    elementos.append(Paragraph("Informações Pessoais", subtitulo_style))
    
    dados_pessoais = [
        ['Campo', 'Informação'],
        ['Nome Completo', idoso.nome],
        ['Idade', f'{idoso.idade} anos'],
        ['CPF', idoso.cpf],
        ['Telefone', idoso.telefone or '-'],
        ['Endereço', idoso.endereco],
        ['Status', 'Ativo' if idoso.ativo else 'Inativo'],
    ]
    
    tabela_pessoais = Table(dados_pessoais, colWidths=[2*inch, 4*inch])
    tabela_pessoais.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066CC')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
    ]))
    elementos.append(tabela_pessoais)
    elementos.append(Spacer(1, 20))
    
    # RESPONSÁVEL
    elementos.append(Paragraph("Responsável", subtitulo_style))
    
    dados_responsavel = [
        ['Campo', 'Informação'],
        ['Nome', idoso.nome_responsavel],
        ['Telefone', idoso.telefone_responsavel],
        ['E-mail', idoso.email_responsavel],
    ]
    
    tabela_responsavel = Table(dados_responsavel, colWidths=[2*inch, 4*inch])
    tabela_responsavel.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066CC')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
    ]))
    elementos.append(tabela_responsavel)
    elementos.append(Spacer(1, 20))
    
    # ESTATÍSTICAS DE SAÚDE (ÚLTIMOS 30 DIAS)
    trinta_dias_atras = timezone.now() - timedelta(days=30)
    dados_saude = DadoSaude.objects.filter(
        idoso=idoso,
        timestamp__gte=trinta_dias_atras
    )
    
    if dados_saude.exists():
        elementos.append(Paragraph("Estatísticas de Saúde (Últimos 30 Dias)", subtitulo_style))
        
        # Calcular estatísticas
        stats_fc = dados_saude.filter(frequencia_cardiaca__isnull=False).aggregate(
            media=Avg('frequencia_cardiaca'),
            minima=Min('frequencia_cardiaca'),
            maxima=Max('frequencia_cardiaca')
        )
        
        stats_pressao_s = dados_saude.filter(pressao_sistolica__isnull=False).aggregate(
            media=Avg('pressao_sistolica'),
            minima=Min('pressao_sistolica'),
            maxima=Max('pressao_sistolica')
        )
        
        stats_pressao_d = dados_saude.filter(pressao_diastolica__isnull=False).aggregate(
            media=Avg('pressao_diastolica'),
            minima=Min('pressao_diastolica'),
            maxima=Max('pressao_diastolica')
        )
        
        stats_saturacao = dados_saude.filter(saturacao_oxigenio__isnull=False).aggregate(
            media=Avg('saturacao_oxigenio'),
            minima=Min('saturacao_oxigenio'),
            maxima=Max('saturacao_oxigenio')
        )
        
        dados_estatisticas = [
            ['Métrica', 'Média', 'Mínima', 'Máxima'],
            ['Freq. Cardíaca (bpm)', 
             f"{stats_fc['media']:.0f}" if stats_fc['media'] else '-',
             f"{stats_fc['minima']:.0f}" if stats_fc['minima'] else '-',
             f"{stats_fc['maxima']:.0f}" if stats_fc['maxima'] else '-'],
            ['Pressão Sistólica (mmHg)', 
             f"{stats_pressao_s['media']:.0f}" if stats_pressao_s['media'] else '-',
             f"{stats_pressao_s['minima']:.0f}" if stats_pressao_s['minima'] else '-',
             f"{stats_pressao_s['maxima']:.0f}" if stats_pressao_s['maxima'] else '-'],
            ['Pressão Diastólica (mmHg)', 
             f"{stats_pressao_d['media']:.0f}" if stats_pressao_d['media'] else '-',
             f"{stats_pressao_d['minima']:.0f}" if stats_pressao_d['minima'] else '-',
             f"{stats_pressao_d['maxima']:.0f}" if stats_pressao_d['maxima'] else '-'],
            ['Saturação O₂ (%)', 
             f"{stats_saturacao['media']:.1f}" if stats_saturacao['media'] else '-',
             f"{stats_saturacao['minima']:.1f}" if stats_saturacao['minima'] else '-',
             f"{stats_saturacao['maxima']:.1f}" if stats_saturacao['maxima'] else '-'],
        ]
        
        tabela_stats = Table(dados_estatisticas, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        tabela_stats.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066CC')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ]))
        elementos.append(tabela_stats)
        elementos.append(Spacer(1, 20))
    
    # ALERTAS RECENTES
    alertas_recentes = Alerta.objects.filter(
        idoso=idoso
    ).order_by('-timestamp')[:10]
    
    if alertas_recentes.exists():
        elementos.append(Paragraph("Alertas Recentes", subtitulo_style))
        
        dados_alertas = [['Data/Hora', 'Tipo', 'Nível', 'Mensagem']]
        
        for alerta in alertas_recentes:
            dados_alertas.append([
                alerta.timestamp.strftime("%d/%m/%Y %H:%M"),
                alerta.get_tipo_display(),
                alerta.get_nivel_display(),
                alerta.mensagem[:50] + '...' if len(alerta.mensagem) > 50 else alerta.mensagem
            ])
        
        tabela_alertas = Table(dados_alertas, colWidths=[1.5*inch, 1.5*inch, 1*inch, 3*inch])
        tabela_alertas.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF9900')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elementos.append(tabela_alertas)
    
    # Observações Médicas
    if idoso.observacoes_medicas:
        elementos.append(Spacer(1, 20))
        elementos.append(Paragraph("Observações Médicas", subtitulo_style))
        elementos.append(Paragraph(idoso.observacoes_medicas, styles['Normal']))
    
    # Rodapé
    elementos.append(Spacer(1, 30))
    elementos.append(Paragraph(
        "<i>Este relatório é confidencial e destina-se exclusivamente ao uso médico e familiar.</i>",
        styles['Normal']
    ))
    
    # Construir PDF
    doc.build(elementos)
    
    # Obter o valor do BytesIO e escrever na resposta
    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="relatorio_{idoso.nome.replace(" ", "_")}_{datetime.now().strftime("%Y%m%d")}.pdf"'
    response.write(pdf)
    
    return response

@login_required
def gerar_relatorio_pdf_geral(request):
    """Gera relatório PDF geral de todos os idosos"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    elementos = []
    styles = getSampleStyleSheet()
    
    titulo_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#0066CC'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    subtitulo_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#004C99'),
        spaceAfter=12,
    )
    
    # Título
    elementos.append(Paragraph("Relatório Geral de Monitoramento", titulo_style))
    elementos.append(Spacer(1, 12))
    
    data_atual = datetime.now().strftime("%d/%m/%Y às %H:%M")
    elementos.append(Paragraph(f"<i>Gerado em: {data_atual}</i>", styles['Normal']))
    elementos.append(Spacer(1, 20))
    
    # Resumo Geral
    total_idosos = Idoso.objects.filter(ativo=True).count()
    total_dispositivos = Dispositivo.objects.filter(ativo=True).count()
    total_alertas = Alerta.objects.filter(visualizado=False).count()
    
    elementos.append(Paragraph("Resumo Geral", subtitulo_style))
    
    dados_resumo = [
        ['Métrica', 'Valor'],
        ['Total de Idosos Ativos', str(total_idosos)],
        ['Dispositivos Ativos', str(total_dispositivos)],
        ['Alertas Pendentes', str(total_alertas)],
    ]
    
    tabela_resumo = Table(dados_resumo, colWidths=[3*inch, 3*inch])
    tabela_resumo.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066CC')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
    ]))
    elementos.append(tabela_resumo)
    elementos.append(Spacer(1, 20))
    
    # Lista de Idosos
    elementos.append(Paragraph("Lista de Idosos Monitorados", subtitulo_style))
    
    idosos = Idoso.objects.filter(ativo=True)
    dados_idosos = [['Nome', 'Idade', 'CPF', 'Responsável', 'Telefone']]
    
    for idoso in idosos:
        dados_idosos.append([
            idoso.nome,
            f"{idoso.idade} anos",
            idoso.cpf,
            idoso.nome_responsavel,
            idoso.telefone_responsavel
        ])
    
    tabela_idosos = Table(dados_idosos, colWidths=[1.5*inch, 0.8*inch, 1.2*inch, 1.5*inch, 1.2*inch])
    tabela_idosos.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066CC')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elementos.append(tabela_idosos)
    
    # Rodapé
    elementos.append(Spacer(1, 30))
    elementos.append(Paragraph(
        "<i>Sistema de Monitoramento de Idosos - IFSP Capivari</i>",
        styles['Normal']
    ))
    
    doc.build(elementos)
    
    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="relatorio_geral_{datetime.now().strftime("%Y%m%d_%H%M")}.pdf"'
    response.write(pdf)
    
    return response

