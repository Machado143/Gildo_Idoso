# monitoramento/urls.py - VERSÃO COMPLETA

from django.urls import path
from . import views

urlpatterns = [
    # Páginas principais
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Idosos
    path('idosos/', views.lista_idosos, name='lista_idosos'),
    path('idosos/adicionar/', views.adicionar_idoso, name='adicionar_idoso'),
    path('idosos/<int:idoso_id>/', views.detalhe_idoso, name='detalhe_idoso'),
    path('idosos/<int:idoso_id>/editar/', views.editar_idoso, name='editar_idoso'),
    path('idosos/<int:idoso_id>/dispositivo/adicionar/', views.adicionar_dispositivo, name='adicionar_dispositivo'),
    path('idosos/<int:idoso_id>/dados/', views.historico_dados, name='historico_dados'),
    
    # Alertas
    path('alertas/', views.lista_alertas, name='lista_alertas'),
    path('alertas/<int:alerta_id>/marcar-lido/', views.marcar_alerta_lido, name='marcar_alerta_lido'),
    
    # Relatórios
    path('relatorios/', views.relatorios, name='relatorios'),
    path('exportar-dados/', views.exportar_dados, name='exportar_dados'),
    
    # URLs PÚBLICAS
    path('registrar/idoso/', views.public_add_idoso, name='public_add_idoso'),
    
    # APIs PARA GRÁFICOS (Tempo Real)
    path('api/graficos/frequencia/', views.api_grafico_frequencia, name='api_grafico_frequencia'),
    path('api/graficos/pressao/', views.api_grafico_pressao, name='api_grafico_pressao'),
    path('api/graficos/alertas/', views.api_grafico_alertas, name='api_grafico_alertas'),
    path('api/graficos/passos/', views.api_grafico_passos, name='api_grafico_passos'),
    
    # RELATÓRIOS PDF
    path('relatorios/pdf/idoso/<int:idoso_id>/', views.gerar_relatorio_pdf_idoso, name='relatorio_pdf_idoso'),
    path('relatorios/pdf/geral/', views.gerar_relatorio_pdf_geral, name='relatorio_pdf_geral'),

    # Gerar dados fictícios (apenas para administradores)
    path('gerar-dados/', views.gerar_dados_ficticios_view, name='gerar_dados'),
]