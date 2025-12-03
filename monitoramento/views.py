# monitoramento/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Idoso, Dispositivo, DadoSaude, Alerta, HistoricoSaude
from .forms import IdosoForm, DispositivoForm

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