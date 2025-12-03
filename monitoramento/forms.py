# monitoramento/forms.py
from django import forms
from .models import Idoso, Dispositivo, DadoSaude, HistoricoSaude

class IdosoForm(forms.ModelForm):
    class Meta:
        model = Idoso
        fields = [
            'nome', 'data_nascimento', 'cpf', 'telefone', 'endereco',
            'nome_responsavel', 'telefone_responsavel', 'email_responsavel',
            'observacoes_medicas'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo do idoso'
            }),
            'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000'
            }),
            'endereco': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Endereço completo'
            }),
            'nome_responsavel': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do responsável'
            }),
            'telefone_responsavel': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000'
            }),
            'email_responsavel': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemplo.com'
            }),
            'observacoes_medicas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Observações médicas relevantes'
            }),
        }

class DispositivoForm(forms.ModelForm):
    class Meta:
        model = Dispositivo
        fields = ['tipo', 'modelo', 'numero_serie']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Modelo do dispositivo'
            }),
            'numero_serie': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de série único'
            }),
        }