from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Idoso, Dispositivo, DadoSaude, Alerta, HistoricoSaude
from .forms import IdosoForm, DispositivoForm
from django.core.paginator import Paginator
import csv
from django.http import HttpResponse


@login_required
def dashboard(request):
    """Dashboard principal com visão geral dos idosos monitorados"""
    idosos = Idoso.objects.filter(ativo=True)
    
    # Estatísticas gerais
    total_idosos = idosos.count()
    dispositivos_ativos = Dispositivo.objects.filter(ativo=True).count()
    alertas_recentes = Alerta.objects.filter(visualizado=False).count()
    
    # Últimos dados de saúde
    ultimos_dados = DadoSaude.objects.select_related('idoso').order_by('-timestamp')[:10]
    
    # Alertas não visualizados
    alertas_pendentes = Alerta.objects.filter(visualizado=False).order_by('-timestamp')[:5]
    
    context = {
        'idosos': idosos,
        'total_idosos': total_idosos,
        'dispositivos_ativos': dispositivos_ativos,
        'alertas_recentes': alertas_recentes,
        'ultimos_dados': ultimos_dados,
        'alertas_pendentes': alertas_pendentes,
    }
    return render(request, 'monitoramento/dashboard.html', context)

@login_required
def lista_idosos(request):
    """Lista todos os idosos cadastrados"""
    idosos = Idoso.objects.all().order_by('nome')
    return render(request, 'monitoramento/lista_idosos.html', {'idosos': idosos})

@login_required
def detalhe_idoso(request, idoso_id):
    """Detalhes de um idoso específico com seus dados de saúde"""
    idoso = get_object_or_404(Idoso, id=idoso_id)
    
    # Dados recentes (últimas 24 horas)
    vinte_quatro_horas_ago = timezone.now() - timedelta(hours=24)
    dados_recentes = DadoSaude.objects.filter(
        idoso=idoso, 
        timestamp__gte=vinte_quatro_horas_ago
    ).order_by('-timestamp')
    
    # Dispositivos do idoso
    dispositivos = Dispositivo.objects.filter(idoso=idoso)
    
    # Alertas recentes
    alertas_recentes = Alerta.objects.filter(idoso=idoso).order_by('-timestamp')[:10]
    
    # Histórico médico
    historico = HistoricoSaude.objects.filter(idoso=idoso).order_by('-data_consulta')[:5]
    
    context = {
        'idoso': idoso,
        'dados_recentes': dados_recentes,
        'dispositivos': dispositivos,
        'alertas_recentes': alertas_recentes,
        'historico': historico,
    }
    return render(request, 'monitoramento/detalhe_idoso.html', context)

@login_required
def adicionar_idoso(request):
    """Adicionar novo idoso ao sistema"""
    if request.method == 'POST':
        form = IdosoForm(request.POST)
        if form.is_valid():
            idoso = form.save()
            messages.success(request, f'Idoso {idoso.nome} cadastrado com sucesso!')
            return redirect('lista_idosos')
    else:
        form = IdosoForm()
    
    return render(request, 'monitoramento/adicionar_idoso.html', {'form': form})

@login_required
def editar_idoso(request, idoso_id):
    """Editar informações de um idoso"""
    idoso = get_object_or_404(Idoso, id=idoso_id)
    
    if request.method == 'POST':
        form = IdosoForm(request.POST, instance=idoso)
        if form.is_valid():
            form.save()
            messages.success(request, f'Dados de {idoso.nome} atualizados!')
            return redirect('detalhe_idoso', idoso_id=idoso.id)
    else:
        form = IdosoForm(instance=idoso)
    
    return render(request, 'monitoramento/editar_idoso.html', {'form': form, 'idoso': idoso})

@login_required
def adicionar_dispositivo(request, idoso_id):
    """Adicionar dispositivo a um idoso"""
    idoso = get_object_or_404(Idoso, id=idoso_id)
    
    if request.method == 'POST':
        form = DispositivoForm(request.POST)
        if form.is_valid():
            dispositivo = form.save(commit=False)
            dispositivo.idoso = idoso
            dispositivo.save()
            messages.success(request, 'Dispositivo cadastrado com sucesso!')
            return redirect('detalhe_idoso', idoso_id=idoso.id)
    else:
        form = DispositivoForm()
    
    return render(request, 'monitoramento/adicionar_dispositivo.html', {
        'form': form, 
        'idoso': idoso
    })

def index(request):
    """Página inicial pública"""
    return render(request, 'monitoramento/index.html')

# Adicione ao final do arquivo monitoramento/views.py

@login_required
def historico_dados(request, idoso_id):
    """Mostra histórico completo de dados de um idoso"""
    idoso = get_object_or_404(Idoso, id=idoso_id)
    dados = DadoSaude.objects.filter(idoso=idoso).order_by('-timestamp')
    
    return render(request, 'monitoramento/historico_dados.html', {
        'idoso': idoso,
        'dados': dados
    })

@login_required
def lista_alertas(request):
    """Lista todos os alertas do sistema"""
    alertas = Alerta.objects.all().order_by('-timestamp')
    return render(request, 'monitoramento/lista_alertas.html', {'alertas': alertas})

@login_required
def marcar_alerta_lido(request, alerta_id):
    """Marca um alerta como visualizado"""
    alerta = get_object_or_404(Alerta, id=alerta_id)
    alerta.visualizado = True
    alerta.data_visualizacao = timezone.now()
    alerta.save()
    
    messages.success(request, 'Alerta marcado como lido!')
    return redirect('lista_alertas')

@login_required
def relatorios(request):
    """Gera relatórios de saúde"""
    idosos = Idoso.objects.filter(ativo=True)
    return render(request, 'monitoramento/relatorios.html', {'idosos': idosos})

@login_required
def exportar_dados(request):
    """Exporta dados em CSV"""
    import csv
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dados_idosos.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Nome', 'Data', 'Frequência', 'Pressão', 'Saturação'])
    
    dados = DadoSaude.objects.all()[:1000]
    for dado in dados:
        writer.writerow([
            dado.idoso.nome,
            dado.timestamp,
            dado.frequencia_cardiaca,
            dado.pressao_arterial,
            dado.saturacao_oxigenio
        ])
    
    return response

@login_required
def historico_dados(request, idoso_id):
    """Mostra histórico completo de dados de um idoso com paginação"""
    idoso = get_object_or_404(Idoso, id=idoso_id)
    
    # Filtrar por período
    dias = request.GET.get('dias', 7)
    data_inicio = timezone.now() - timedelta(days=int(dias))
    
    dados = DadoSaude.objects.filter(
        idoso=idoso, 
        timestamp__gte=data_inicio
    ).order_by('-timestamp')
    
    # Paginação
    paginator = Paginator(dados, 20)  # 20 itens por página
    page = request.GET.get('page')
    dados_paginados = paginator.get_page(page)
    
    return render(request, 'monitoramento/historico_dados.html', {
        'idoso': idoso,
        'dados': dados_paginados,
        'dias': dias
    })
@login_required
def lista_alertas(request):
    """Lista todos os alertas com filtros"""
    alertas = Alerta.objects.all().order_by('-timestamp')
    
    # Filtros
    nivel = request.GET.get('nivel')
    tipo = request.GET.get('tipo')
    visualizado = request.GET.get('visualizado')
    
    if nivel:
        alertas = alertas.filter(nivel=nivel)
    if tipo:
        alertas = alertas.filter(tipo=tipo)
    if visualizado:
        alertas = alertas.filter(visualizado=visualizado == 'true')
    
    return render(request, 'monitoramento/lista_alertas.html', {
        'alertas': alertas[:100],  # Limita a 100 resultados
        'filtros': {'nivel': nivel, 'tipo': tipo, 'visualizado': visualizado}
    })

@login_required
def marcar_alerta_lido(request, alerta_id):
    """Marca alerta como visualizado"""
    alerta = get_object_or_404(Alerta, id=alerta_id)
    alerta.visualizado = True
    alerta.data_visualizacao = timezone.now()
    alerta.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    messages.success(request, '✅ Alerta marcado como lido!')
    return redirect('lista_alertas')


@login_required
def relatorios(request):
    """Dashboard de relatórios"""
    idosos = Idoso.objects.filter(ativo=True)
    
    # Estatísticas gerais
    total_alertas = Alerta.objects.count()
    alertas_criticos = Alerta.objects.filter(nivel='critico').count()
    media_frequencia = DadoSaude.objects.filter(
        frequencia_cardiaca__isnull=False
    ).aggregate(avg=models.Avg('frequencia_cardiaca'))
    
    return render(request, 'monitoramento/relatorios.html', {
        'idosos': idosos,
        'total_alertas': total_alertas,
        'alertas_criticos': alertas_criticos,
        'media_frequencia': media_frequencia['avg']
    })

@login_required
def exportar_dados(request):
    """Exporta dados em CSV"""
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="dados_idosos.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Nome do Idoso', 'Data/Hora', 'Frequência Cardíaca', 
                     'Pressão Arterial', 'Saturação O₂', 'Temperatura', 
                     'Passos', 'Queda Detectada', 'Emergência'])
    
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