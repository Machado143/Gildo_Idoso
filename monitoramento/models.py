# monitoramento/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date

class Idoso(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=20, blank=True)
    endereco = models.TextField()
    nome_responsavel = models.CharField(max_length=100)
    telefone_responsavel = models.CharField(max_length=20)
    email_responsavel = models.EmailField()
    observacoes_medicas = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(default=timezone.now)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)

    def __str__(self):
        return f"{self.nome} - {self.cpf}"

    @property
    def idade(self):
        hoje = date.today()
        nascimento = self.data_nascimento
        idade = hoje.year - nascimento.year
        if hoje.month < nascimento.month or (hoje.month == nascimento.month and hoje.day < nascimento.day):
            idade -= 1
        return idade

class Dispositivo(models.Model):
    TIPO_DISPOSITIVO = [
        ('relogio', 'Relógio Inteligente'),
        ('pulseira', 'Pulseira Fitness'),
        ('sensor', 'Sensor Corporal'),
        ('outro', 'Outro'),
    ]

    idoso = models.ForeignKey(Idoso, on_delete=models.CASCADE, related_name='dispositivos')
    tipo = models.CharField(max_length=20, choices=TIPO_DISPOSITIVO)
    modelo = models.CharField(max_length=100)
    numero_serie = models.CharField(max_length=50, unique=True)
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(default=timezone.now)
    ultima_sincronizacao = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.modelo}"

class DadoSaude(models.Model):
    idoso = models.ForeignKey(Idoso, on_delete=models.CASCADE, related_name='dados_saude')
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, related_name='dados')
    
    frequencia_cardiaca = models.IntegerField(null=True, blank=True)
    pressao_sistolica = models.IntegerField(null=True, blank=True)
    pressao_diastolica = models.IntegerField(null=True, blank=True)
    saturacao_oxigenio = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    temperatura = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    
    passos = models.IntegerField(null=True, blank=True)
    distancia = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    calorias = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    
    queda_detectada = models.BooleanField(default=False)
    botao_emergencia = models.BooleanField(default=False)
    
    timestamp = models.DateTimeField(default=timezone.now)
    bateria_dispositivo = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Dados {self.idoso.nome} - {self.timestamp.strftime('%d/%m/%Y %H:%M')}"

    @property
    def pressao_arterial(self):
        if self.pressao_sistolica and self.pressao_diastolica:
            return f"{self.pressao_sistolica}/{self.pressao_diastolica}"
        return None

class Alerta(models.Model):
    NIVEL_ALERTA = [
        ('baixo', 'Baixo'),
        ('medio', 'Médio'),
        ('alto', 'Alto'),
        ('critico', 'Crítico'),
    ]

    TIPO_ALERTA = [
        ('frequencia_cardiaca', 'Frequência Cardíaca'),
        ('pressao_arterial', 'Pressão Arterial'),
        ('queda', 'Queda Detectada'),
        ('emergencia', 'Botão de Emergência'),
        ('inatividade', 'Inatividade Prolongada'),
        ('bateria_baixa', 'Bateria Baixa'),
        ('desconexao', 'Desconexão do Dispositivo'),
    ]

    idoso = models.ForeignKey(Idoso, on_delete=models.CASCADE, related_name='alertas')
    tipo = models.CharField(max_length=30, choices=TIPO_ALERTA)
    nivel = models.CharField(max_length=10, choices=NIVEL_ALERTA)
    mensagem = models.TextField()
    dado_saude = models.ForeignKey(DadoSaude, on_delete=models.CASCADE, null=True, blank=True)
    
    visualizado = models.BooleanField(default=False)
    data_visualizacao = models.DateTimeField(null=True, blank=True)
    notificacao_email = models.BooleanField(default=False)
    notificacao_sms = models.BooleanField(default=False)
    
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Alerta {self.get_tipo_display()} - {self.idoso.nome}"

class HistoricoSaude(models.Model):
    idoso = models.ForeignKey(Idoso, on_delete=models.CASCADE, related_name='historico')
    data_consulta = models.DateField()
    tipo_consulta = models.CharField(max_length=100)
    medico = models.CharField(max_length=100)
    diagnostico = models.TextField()
    medicamentos = models.TextField(blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-data_consulta']

    def __str__(self):
        return f"Consulta {self.idoso.nome} - {self.data_consulta}"