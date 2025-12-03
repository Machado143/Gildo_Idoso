from django.test import TestCase
from django.contrib.auth.models import User
from .models import Idoso, Alerta
from .utils import validar_cpf

class IdosoModelTest(TestCase):
    def setUp(self):
        self.idoso = Idoso.objects.create(
            nome="Maria Silva",
            data_nascimento="1950-03-15",
            cpf="123.456.789-00",
            nome_responsavel="João Silva",
            telefone_responsavel="(11) 99876-5432",
            email_responsavel="joao@exemplo.com"
        )
    
    def test_idade_calculada(self):
        self.assertEqual(self.idoso.idade, 74)  # Ajuste conforme ano atual
    
    def test_str_representation(self):
        self.assertEqual(str(self.idoso), "Maria Silva - 123.456.789-00")

class APIEndpointsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_login(self.user)
    
    def test_dashboard_access(self):
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
    
    def test_api_idosos_list(self):
        response = self.client.get('/api/idosos/')
        self.assertEqual(response.status_code, 200)