from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Idoso, Dispositivo, DadoSaude, Alerta
from datetime import datetime, timedelta

class IdosoModelTest(TestCase):
    def test_idade_calculada(self):
        idoso = Idoso.objects.create(
            nome="Teste",
            data_nascimento="1950-01-01",
            cpf="123.456.789-00",
            nome_responsavel="Resp",
            telefone_responsavel="(11) 99999-9999",
            email_responsavel="test@email.com",
            latitude=-23.550520,
            longitude=-46.633308
        )
        self.assertEqual(idoso.idade, 74)  # Ajuste conforme ano atual

class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.idoso = Idoso.objects.create(
            nome="Maria Teste",
            data_nascimento="1955-05-15",
            cpf="987.654.321-00",
            nome_responsavel="João",
            telefone_responsavel="(11) 98888-8888",
            email_responsavel="joao@email.com",
            ativo=True,
            latitude=-23.550520,
            longitude=-46.633308
        )
    
    def test_dashboard_autenticado(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
    
    def test_public_add_idoso_get(self):
        response = self.client.get('/registrar/idoso/')
        self.assertEqual(response.status_code, 200)
    
    def test_public_add_idoso_post(self):
        data = {
            'nome': 'Novo Idoso',
            'data_nascimento': '1940-03-10',
            'cpf': '111.222.333-99',
            'endereco': 'Rua Teste, 123',
            'nome_responsavel': 'Resp Teste',
            'telefone_responsavel': '(11) 99999-9999',
            'email_responsavel': 'resp@teste.com',
            'observacoes_medicas': 'Teste',
            'latitude': -23.550520,
            'longitude': -46.633308
        }
        response = self.client.post('/registrar/idoso/', data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Idoso.objects.get(cpf='111.222.333-99').ativo)

class APITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='apiuser', password='apipass')
        self.client.login(username='apiuser', password='apipass')
        self.idoso = Idoso.objects.create(
            nome="API Teste",
            data_nascimento="1948-08-20",
            cpf="111.111.111-11",
            nome_responsavel="Resp API",
            telefone_responsavel="(11) 97777-7777",
            email_responsavel="api@email.com",
            latitude=-23.550520,
            longitude=-46.633308
        )
        self.dispositivo = Dispositivo.objects.create(
            idoso=self.idoso,
            tipo='relogio',
            modelo='Test Watch',
            numero_serie='TEST123'
        )
    
    def test_api_idosos_list(self):
        response = self.client.get('/api/idosos/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 1)