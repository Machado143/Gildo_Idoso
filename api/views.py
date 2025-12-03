from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from monitoramento.models import Idoso, Dispositivo, DadoSaude, Alerta
from .serializers import *

class IdosoViewSet(viewsets.ModelViewSet):
    queryset = Idoso.objects.all()
    serializer_class = IdosoSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def receber_dados(self, request, pk=None):
        """Endpoint para dispositivos enviarem dados"""
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
            
            # Gerar alertas automáticos
            self.gerenciar_alertas(dado)
            
            return Response({'status': 'dado recebido'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def gerenciar_alertas(self, dado):
        """Lógica de geração de alertas baseada nos dados"""
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