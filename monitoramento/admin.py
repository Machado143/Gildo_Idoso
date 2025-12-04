from django.contrib import admin
from django.utils.html import format_html
from .models import Idoso, Dispositivo, DadoSaude, Alerta, HistoricoSaude
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.management import call_command
from django.urls import path
from django.http import HttpResponseRedirect

@admin.register(Idoso)
class IdosoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'idade', 'cpf', 'nome_responsavel', 'status_ativo', 'data_cadastro', 'localizacao']
    list_filter = ['ativo', 'data_cadastro']
    search_fields = ['nome', 'cpf', 'nome_responsavel', 'email_responsavel']
    readonly_fields = ['data_cadastro', 'idade']
    list_editable = []  # REMOVIDO O ATRIBUTO PROBLEMÁTICO
    
    def status_ativo(self, obj):
        if obj.ativo:
            return format_html('<span style="color: green;">✔ Ativo</span>')
        return format_html('<span style="color: orange;">⏳ Pendente</span>')
    status_ativo.short_description = 'Status'
    
    def localizacao(self, obj):
        if obj.latitude and obj.longitude:
            return format_html('<a href="https://maps.google.com/?q={},{}">📍</a>', obj.latitude, obj.longitude)
        return '-'
    localizacao.allow_tags = True

@admin.register(Dispositivo)
class DispositivoAdmin(admin.ModelAdmin):
    list_display = ['idoso', 'tipo', 'modelo', 'numero_serie', 'ativo', 'data_cadastro']
    list_filter = ['tipo', 'ativo', 'data_cadastro']
    search_fields = ['modelo', 'numero_serie', 'idoso__nome']

@admin.register(DadoSaude)
class DadoSaudeAdmin(admin.ModelAdmin):
    list_display = ['idoso', 'timestamp', 'frequencia_cardiaca', 'pressao_arterial', 'saturacao_oxigenio', 'temperatura']
    list_filter = ['timestamp', 'queda_detectada']
    search_fields = ['idoso__nome']
    readonly_fields = ['timestamp', 'pressao_arterial']

@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ['idoso', 'tipo', 'nivel', 'visualizado', 'timestamp']
    list_filter = ['tipo', 'nivel', 'visualizado', 'timestamp']
    search_fields = ['idoso__nome', 'mensagem']

@admin.register(HistoricoSaude)
class HistoricoSaudeAdmin(admin.ModelAdmin):
    list_display = ['idoso', 'data_consulta', 'tipo_consulta', 'medico']
    list_filter = ['data_consulta', 'tipo_consulta']
    search_fields = ['idoso__nome', 'medico', 'diagnostico']

# View para gerar dados fictícios
def gerar_dados_ficticios_view(request):
    if request.method == 'POST':
        try:
            idosos = int(request.POST.get('idosos', 5))
            dias = int(request.POST.get('dias', 7))
            call_command('gerar_dados_ficticios', idosos=idosos, dias=dias)
            messages.success(request, f'✅ Dados fictícios gerados: {idosos} idosos, {dias} dias!')
        except Exception as e:
            messages.error(request, f'❌ Erro ao gerar dados: {str(e)}')
        return redirect('admin:gerar_dados_ficticios')
    
    context = {
        'title': 'Gerar Dados Fictícios',
    }
    return render(request, 'admin/gerar_dados.html', context)

# Classe Admin customizada
class MonitoramentoAdminSite(admin.AdminSite):
    site_header = "Monitoramento de Idosos"
    site_title = "Administração"
    index_title = "Painel de Controle"

# Criar instância customizada
admin_site = MonitoramentoAdminSite(name='monitoramento-admin')

# Adicionar a URL customizada
def get_admin_urls():
    from django.urls import path
    urls = [
        path('gerar-dados/', gerar_dados_ficticios_view, name='gerar_dados_ficticios'),
    ]
    return urls

# Registrar os modelos normais
admin.site.register(Idoso, IdosoAdmin)
admin.site.register(Dispositivo, DispositivoAdmin)
admin.site.register(DadoSaude, DadoSaudeAdmin)
admin.site.register(Alerta, AlertaAdmin)
admin.site.register(HistoricoSaude, HistoricoSaudeAdmin)