# monitoramento/management/commands/gerar_dados_ficticios.py
import random
from django.core.management.base import BaseCommand
from monitoramento.models import Idoso, Dispositivo, DadoSaude, Alerta
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Gera dados fictícios para testes'

    def add_arguments(self, parser):
        parser.add_argument('--idosos', type=int, default=5, help='Número de idosos')
        parser.add_argument('--dias', type=int, default=7, help='Dias de histórico')

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('🎲 Gerando dados fictícios...'))
        
        for i in range(options['idosos']):
            # Criar idoso
            idoso = Idoso.objects.create(
                nome=f'Idoso Teste {i+1}',
                data_nascimento=timezone.now() - timedelta(days=365*70 + random.randint(0, 365*10)),
                cpf=f'000.000.000-{i:02d}',
                endereco=f'Rua Teste, {i+100} - Cidade',
                nome_responsavel=f'Responsável {i+1}',
                telefone_responsavel=f'(11) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}',
                email_responsavel=f'resp{i}@teste.com',
                ativo=True,
            )
            
            # Criar dispositivo
            dispositivo = Dispositivo.objects.create(
                idoso=idoso,
                tipo=random.choice(['relogio', 'pulseira', 'sensor']),
                modelo=f'Modelo {random.choice(["Apple Watch", "Samsung Galaxy", "Xiaomi Mi"])}',
                numero_serie=f'DEVICE-{idoso.id:04d}',
                ativo=True,
            )
            
            # Gerar dados históricos
            for dia in range(options['dias']):
                for hora in range(0, 24, 3):  # A cada 3 horas
                    timestamp = timezone.now() - timedelta(days=dia, hours=hora)
                    
                    # Dados normais com variações realistas
                    fc = random.randint(65, 95)
                    sistolica = random.randint(110, 140)
                    diastolica = random.randint(70, 90)
                    saturacao = round(random.uniform(95, 99), 1)
                    temperatura = round(random.uniform(36.0, 37.5), 1)
                    passos = random.randint(1000, 8000)
                    
                    # 5% de chance de emergência
                    queda = random.random() < 0.05
                    emergencia = random.random() < 0.05
                    
                    dado = DadoSaude.objects.create(
                        idoso=idoso,
                        dispositivo=dispositivo,
                        frequencia_cardiaca=fc,
                        pressao_sistolica=sistolica,
                        pressao_diastolica=diastolica,
                        saturacao_oxigenio=saturacao,
                        temperatura=temperatura,
                        passos=passos,
                        queda_detectada=queda,
                        botao_emergencia=emergencia,
                        timestamp=timestamp,
                    )
                    
                    # Criar alertas para emergências
                    if queda:
                        Alerta.objects.create(
                            idoso=idoso,
                            tipo='queda',
                            nivel='critico',
                            mensagem='🚨 Queda detectada! Verifique imediatamente!',
                            dado_saude=dado,
                        )
                    elif emergencia:
                        Alerta.objects.create(
                            idoso=idoso,
                            tipo='emergencia',
                            nivel='critico',
                            mensagem='🆘 Botão de emergência acionado!',
                            dado_saude=dado,
                        )
                    elif fc > 120 or fc < 50:
                        Alerta.objects.create(
                            idoso=idoso,
                            tipo='frequencia_cardiaca',
                            nivel='alto',
                            mensagem=f'❤️ Frequência cardíaca anormal: {fc} bpm',
                            dado_saude=dado,
                        )
        
        self.stdout.write(self.style.SUCCESS('✅ Dados fictícios gerados com sucesso!'))
        self.stdout.write(self.style.SUCCESS(f'📊 {options["idosos"]} idosos criados'))
        self.stdout.write(self.style.SUCCESS(f'📅 {options["dias"]} dias de histórico'))