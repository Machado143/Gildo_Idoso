from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('idosos/', views.lista_idosos, name='lista_idosos'),
    path('idosos/adicionar/', views.adicionar_idoso, name='adicionar_idoso'),
    path('idosos/<int:idoso_id>/', views.detalhe_idoso, name='detalhe_idoso'),
    path('idosos/<int:idoso_id>/editar/', views.editar_idoso, name='editar_idoso'),
    path('idosos/<int:idoso_id>/dispositivo/adicionar/', views.adicionar_dispositivo, name='adicionar_dispositivo'),
    
    # NOVAS ROTAS
    path('idosos/<int:idoso_id>/dados/', views.historico_dados, name='historico_dados'),
    path('alertas/', views.lista_alertas, name='lista_alertas'),
    path('alertas/<int:alerta_id>/marcar-lido/', views.marcar_alerta_lido, name='marcar_alerta_lido'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('exportar-dados/', views.exportar_dados, name='exportar_dados'),
]