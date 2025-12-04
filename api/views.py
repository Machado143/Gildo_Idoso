from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
import random
from django.http import JsonResponse
from monitoramento.models import Idoso, Dispositivo, DadoSaude, Alerta, HistoricoSaude
from .serializers import *

class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class IdosoViewSet(viewsets.ModelViewSet):
    queryset = Idoso.objects.all()
    serializer_class = IdosoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination
    
    def get_queryset(self):
        queryset = Idoso.objects.all()
        ativo = self.request.query_params.get('ativo')
        if ativo is not None:
            queryset = queryset.filter(ativo=ativo.lower() == 'true')
        return queryset
    
    @action(detail=True, methods=['post'])
    def ativar(self, request, pk=None):
        idoso = self.get_object()
        idoso.ativo = True
        idoso.save()
        return Response({'status': 'idoso ativado'})
    
    @action(detail=True, methods=['post'])
    def receber_dados(self, request, pk=None):
        idoso = self.get_object()
        dispositivo_id = request.data.get('dispositivo_id')
        
        try:
            dispositivo = Dispositivo.objects.get(
                idoso=idoso, 
                numero_serie=dispositivo_id,
                ativo=True
            )
            
            dado = DadoSaude.objects.create(
                idoso=idoso,
                dispositivo=dispositivo,
                **request.data
            )
            
            # Gerar alertas automaticamente
            self.gerenciar_alertas(dado)
            
            return Response({'status': 'dado recebido', 'id': dado.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def gerenciar_alertas(self, dado):
        if dado.frequencia_cardiaca and (dado.frequencia_cardiaca > 120 or dado.frequencia_cardiaca < 50):
            Alerta.objects.create(
                idoso=dado.idoso,
                tipo='frequencia_cardiaca',
                nivel='alto',
                mensagem=f'Frequência cardíaca anormal: {dado.frequencia_cardiaca} bpm',
                dado_saude=dado
            )
        
        if dado.queda_detectada:
            Alerta.objects.create(
                idoso=dado.idoso,
                tipo='queda',
                nivel='critico',
                mensagem='QUEDA DETECTADA! Verifique imediatamente!',
                dado_saude=dado
            )

class DispositivoViewSet(viewsets.ModelViewSet):
    queryset = Dispositivo.objects.all()
    serializer_class = DispositivoSerializer
    permission_classes = [IsAuthenticated]

class DadoSaudeViewSet(viewsets.ModelViewSet):
    queryset = DadoSaude.objects.all()
    serializer_class = DadoSaudeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = DadoSaude.objects.all()
        idoso_id = self.request.query_params.get('idoso')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if idoso_id:
            queryset = queryset.filter(idoso_id=idoso_id)
        if start_date:
            queryset = queryset.filter(timestamp__gte=start_date)
        if end_date:
            queryset = queryset.filter(timestamp__lte=end_date)
        
        return queryset

class AlertaViewSet(viewsets.ModelViewSet):
    queryset = Alerta.objects.all()
    serializer_class = AlertaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Alerta.objects.all()
        visualizado = self.request.query_params.get('visualizado')
        nivel = self.request.query_params.get('nivel')
        
        if visualizado is not None:
            queryset = queryset.filter(visualizado=visualizado.lower() == 'true')
        if nivel:
            queryset = queryset.filter(nivel=nivel)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def marcar_lido(self, request, pk=None):
        alerta = self.get_object()
        alerta.visualizado = True
        alerta.data_visualizacao = timezone.now()
        alerta.save()
        return Response({'status': 'alerta marcado como lido'})

class HistoricoSaudeViewSet(viewsets.ModelViewSet):
    queryset = HistoricoSaude.objects.all()
    serializer_class = HistoricoSaudeSerializer
    permission_classes = [IsAuthenticated]

@api_view(['GET'])
@permission_classes([AllowAny])
def api_docs(request):
    return Response({
        'endpoints': {
            'idosos': '/api/idosos/',
            'dispositivos': '/api/dispositivos/',
            'dados_saude': '/api/dados-saude/',
            'alertas': '/api/alertas/',
            'historico': '/api/historico/'
        },
        'autenticacao': 'Token ou Session Auth',
        'documentacao': 'Use /api/ para testar endpoints'
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_alertas_emergencia(request):
    """Retorna alertas de emergência não visualizados para atualização em tempo real"""
    idoso_id = request.GET.get('idoso')
    
    alertas = Alerta.objects.filter(
        visualizado=False,
        nivel='critico'
    ).order_by('-timestamp')[:10]
    
    if idoso_id:
        alertas = alertas.filter(idoso_id=idoso_id)
    
    return JsonResponse({
        'emergencias': [{
            'id': alerta.id,
            'idoso_nome': alerta.idoso.nome,
            'idoso_id': alerta.idoso.id,
            'tipo': alerta.get_tipo_display(),
            'mensagem': alerta.mensagem,
            'timestamp': alerta.timestamp.strftime('%d/%m/%Y %H:%M:%S'),
            'queda': alerta.tipo == 'queda',
            'emergencia': alerta.tipo == 'emergencia',
        } for alerta in alertas]
    })