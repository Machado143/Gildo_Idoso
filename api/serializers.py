from rest_framework import serializers
from monitoramento.models import Idoso, Dispositivo, DadoSaude, Alerta

class IdosoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idoso
        fields = '__all__'

class DadoSaudeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DadoSaude
        fields = '__all__'
        read_only_fields = ['timestamp']

class AlertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alerta
        fields = '__all__'