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
]