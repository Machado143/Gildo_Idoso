# monitoramento/admin.py
from django.contrib import admin
from .models import Idoso, Dispositivo, DadoSaude, Alerta, HistoricoSaude

@admin.register(Idoso)
class IdosoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'idade', 'cpf', 'nome_responsavel', 'ativo', 'data_cadastro']
    list_filter = ['ativo', 'data_cadastro']
    search_fields = ['nome', 'cpf', 'nome_responsavel', 'email_responsavel']
    readonly_fields = ['data_cadastro', 'idade']

@admin.register(Dispositivo)
class DispositivoAdmin(admin.ModelAdmin):
    list_display = ['idoso', 'tipo', 'modelo', 'numero_serie', 'ativo', 'data_cadastro']
    list_filter = ['tipo', 'ativo', 'data_cadastro']
    search_fields = ['modelo', 'numero_serie', 'idoso__nome']

@admin.register(DadoSaude)
class DadoSaudeAdmin(admin.ModelAdmin):
    list_display = ['idoso', 'timestamp', 'frequencia_cardiaca', 'pressao_arterial', 'saturacao_oxigenio']
    list_filter = ['timestamp', 'queda_detectada']
    search_fields = ['idoso__nome']
    readonly_fields = ['timestamp']

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