from rest_framework import serializers
from monitoramento.models import Idoso, Dispositivo, DadoSaude, Alerta, HistoricoSaude

class IdosoSerializer(serializers.ModelSerializer):
    idade = serializers.ReadOnlyField()
    dispositivos_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Idoso
        fields = '__all__'
    
    def get_dispositivos_count(self, obj):
        return obj.dispositivos.count()

class DispositivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispositivo
        fields = '__all__'

class DadoSaudeSerializer(serializers.ModelSerializer):
    pressao_arterial = serializers.ReadOnlyField()
    
    class Meta:
        model = DadoSaude
        fields = '__all__'
        read_only_fields = ['timestamp']

class AlertaSerializer(serializers.ModelSerializer):
    idoso_nome = serializers.CharField(source='idoso.nome', read_only=True)
    
    class Meta:
        model = Alerta
        fields = '__all__'

class HistoricoSaudeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoSaude
        fields = '__all__'