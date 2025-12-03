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
    idosos_data = [
        {
            'nome': 'Maria Silva Santos',
            'data_nascimento': '1950-03-15',
            'cpf': '123.456.789-00',
            'telefone': '(11) 98765-4321',
            'endereco': 'Rua das Flores, 123 - Jardim Primavera - São Paulo/SP',
            'nome_responsavel': 'João Silva',
            'telefone_responsavel': '(11) 99876-5432',
            'email_responsavel': 'joao.silva@email.com',
            'observacoes_medicas': 'Hipertensão controlada, diabetes tipo 2'
        }
    ]
    
    idosos = []
    for data in idosos_data:
        idoso, created = Idoso.objects.get_or_create(cpf=data['cpf'], defaults=data)
        idosos.append(idoso)
        print(f"✓ Idoso: {idoso.nome}")
    
    return idosos

def criar_dispositivos(idosos):
    dispositivos_data = [
        {'idoso': idosos[0], 'tipo': 'relogio', 'modelo': 'Apple Watch Series 8', 'numero_serie': 'AW8MSS001'}
    ]
    
    for data in dispositivos_data:
        dispositivo, created = Dispositivo.objects.get_or_create(numero_serie=data['numero_serie'], defaults=data)
        print(f"✓ Dispositivo: {dispositivo.modelo}")

def main():
    print("Populando banco de dados...")
    criar_usuario_admin()
    idosos = criar_idosos()
    criar_dispositivos(idosos)
    print("Banco populado com sucesso!")

if __name__ == '__main__':
    main()