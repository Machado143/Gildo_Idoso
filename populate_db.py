#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'idosos_monitoramento.settings')
django.setup()

from django.contrib.auth.models import User
from monitoramento.models import Idoso, Dispositivo, DadoSaude, Alerta, HistoricoSaude

def criar_usuario_admin():
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@exemplo.com', 'admin123')
        print("✓ Usuário admin criado (admin/admin123)")
    else:
        print("✓ Usuário admin já existe")

def criar_idosos():
    if Idoso.objects.filter(cpf='111.222.333-44').exists():
        print("✓ Idosos de demonstração já existem")
        return
    
    print("Criando 3 idosos com dispositivos e 30 dias de dados...")
    
    idosos_data = [
        {
            'nome': 'José da Silva',
            'data_nascimento': '1948-05-12',
            'cpf': '111.222.333-44',
            'telefone': '(11) 98765-1111',
            'endereco': 'Rua das Acácias, 45 - São Paulo/SP',
            'nome_responsavel': 'Maria Silva',
            'telefone_responsavel': '(11) 99876-1111',
            'email_responsavel': 'maria.silva@email.com',
            'observacoes_medicas': 'Hipertensão, diabetes tipo 2',
            'latitude': -23.550520,
            'longitude': -46.633308
        },
        {
            'nome': 'Ana Maria Santos',
            'data_nascimento': '1952-08-23',
            'cpf': '222.333.444-55',
            'telefone': '(11) 98765-2222',
            'endereco': 'Avenida Paulista, 1000 - São Paulo/SP',
            'nome_responsavel': 'Carlos Santos',
            'telefone_responsavel': '(11) 99876-2222',
            'email_responsavel': 'carlos.santos@email.com',
            'observacoes_medicas': 'Arritmia cardíaca',
            'latitude': -23.561414,
            'longitude': -46.655881
        },
        {
            'nome': 'Mário Costa',
            'data_nascimento': '1945-12-01',
            'cpf': '333.444.555-66',
            'telefone': '(11) 98765-3333',
            'endereco': 'Rua Augusta, 500 - São Paulo/SP',
            'nome_responsavel': 'Luciana Costa',
            'telefone_responsavel': '(11) 99876-3333',
            'email_responsavel': 'luciana.costa@email.com',
            'observacoes_medicas': 'Parkinson, tensão alta',
            'latitude': -23.556702,
            'longitude': -46.662565
        }
    ]

    for data in idosos_data:
        idoso = Idoso.objects.create(**data)
        
        dispositivo = Dispositivo.objects.create(
            idoso=idoso,
            tipo='relogio',
            modelo='Apple Watch Series 9',
            numero_serie=f"AW9-{idoso.cpf.replace('.', '').replace('-', '')}"
        )
        
        # Criar 30 dias de dados
        agora = datetime.now()
        for i in range(30):
            for hora in [8, 12, 16, 20]:
                timestamp = agora - timedelta(days=i, hours=agora.hour-hora)
                
                freq = random.randint(60, 85) if 'José' in idoso.nome else random.randint(65, 90)
                if random.random() < 0.05:
                    freq = random.randint(100, 120)
                
                DadoSaude.objects.create(
                    idoso=idoso,
                    dispositivo=dispositivo,
                    frequencia_cardiaca=freq,
                    pressao_sistolica=random.randint(120, 140),
                    pressao_diastolica=random.randint(70, 90),
                    saturacao_oxigenio=round(random.uniform(95, 99), 1),
                    temperatura=round(random.uniform(36.0, 37.2), 1),
                    passos=random.randint(2000, 7000),
                    queda_detectada=random.random() < 0.01,
                    botao_emergencia=False,
                    bateria_dispositivo=random.randint(20, 100)
                )
        
        print(f"✓ {idoso.nome} + dispositivo + 30 dias de dados")

def main():
    print("Populando banco de dados...")
    criar_usuario_admin()
    criar_idosos()
    print("✅ Banco populado com sucesso!")

if __name__ == '__main__':
    main()