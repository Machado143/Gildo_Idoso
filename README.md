# 📊 Sistema de Monitoramento de Saúde para Idosos

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.1+-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Sistema completo de monitoramento em tempo real para acompanhamento de saúde de idosos**

[Demonstração](https://seu-projeto.render.com) • [Documentação da API](#-api-rest) • [Reportar Bug](https://github.com/seu-usuario/projeto/issues)

</div>

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias-utilizadas)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Uso](#-uso)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [API REST](#-api-rest)
- [Deploy](#-deploy)
- [Testes](#-testes)
- [Contribuição](#-contribuindo)
- [Licença](#-licença)
- [Contato](#-contato)

---

## 🎯 Sobre o Projeto

O **Sistema de Monitoramento de Saúde para Idosos** é uma plataforma web desenvolvida para facilitar o acompanhamento contínuo de dados vitais de idosos, proporcionando segurança e tranquilidade para familiares e cuidadores.

### 🌟 Destaques

- 📊 **Dashboard Interativo** com gráficos em tempo real
- 🚨 **Sistema de Alertas Automáticos** para situações críticas
- 📱 **Interface Responsiva** otimizada para desktop e mobile
- 📄 **Geração de Relatórios** em PDF e CSV
- 🔐 **Sistema de Autenticação** completo
- 🔌 **API REST** documentada para integração com dispositivos IoT

---

## ✨ Funcionalidades

### 👥 Gestão de Idosos
- ✅ Cadastro completo de idosos e responsáveis
- ✅ Histórico médico e observações
- ✅ Vinculação de múltiplos dispositivos
- ✅ Geolocalização integrada

### 📊 Monitoramento de Saúde
- ❤️ Frequência cardíaca
- 🩺 Pressão arterial (sistólica/diastólica)
- 🫁 Saturação de oxigênio
- 🌡️ Temperatura corporal
- 🚶 Contador de passos e atividades
- 🔋 Nível de bateria dos dispositivos

### 🚨 Sistema de Alertas
- 🔴 **Crítico**: Quedas e emergências
- 🟠 **Alto**: Valores anormais de sinais vitais
- 🟡 **Médio**: Inatividade prolongada
- 🟢 **Baixo**: Bateria fraca, desconexão

### 📈 Relatórios e Análises
- 📄 Relatórios individuais em PDF
- 📊 Relatório geral consolidado
- 💾 Exportação de dados em CSV
- 📉 Gráficos de tendências e médias

### 🎨 Interface Moderna
- 🌐 Design responsivo (Mobile-First)
- 🎨 Paleta azul profissional
- ⚡ Atualização automática em tempo real
- 🔔 Notificações push para emergências

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.11+**
- **Django 5.1.4** - Framework web
- **Django REST Framework** - API REST
- **PostgreSQL 15+** - Banco de dados
- **Gunicorn** - Servidor WSGI

### Frontend
- **HTML5 / CSS3**
- **Bootstrap 5.3** - Framework CSS
- **JavaScript (ES6+)**
- **Chart.js** - Gráficos interativos
- **Font Awesome 6** - Ícones

### Bibliotecas Python
```python
Django==5.1.4
djangorestframework==3.14.0
psycopg2-binary==2.9.9
python-decouple==3.8
dj-database-url==2.1.0
whitenoise==6.6.0
gunicorn==21.2.0
reportlab==4.0.7
django-crispy-forms==2.1
crispy-bootstrap5==2.0.0
```

### DevOps
- **Render.com** - Plataforma de deploy
- **WhiteNoise** - Servir arquivos estáticos
- **Git** - Controle de versão

---

## 📦 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- PostgreSQL 15+ (para produção)
- Git
- Virtualenv (recomendado)

---

## 🚀 Instalação

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/seu-usuario/monitoramento-idosos.git
cd monitoramento-idosos
```

### 2️⃣ Crie um ambiente virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Segurança
SECRET_KEY=sua-chave-secreta-super-segura-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Banco de Dados (Desenvolvimento - SQLite)
DATABASE_URL=sqlite:///db.sqlite3

# Banco de Dados (Produção - PostgreSQL)
# DATABASE_URL=postgresql://usuario:senha@host:5432/nome_banco

# Email (Opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=seu-email@gmail.com
EMAIL_PASS=sua-senha-de-app
DEFAULT_FROM_EMAIL=noreply@monitoramento.com
```

### 5️⃣ Execute as migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Crie um superusuário

```bash
python manage.py createsuperuser
```

### 7️⃣ (Opcional) Popule com dados de teste

```bash
python manage.py shell -c "
from monitoramento.management.commands.gerar_dados_ficticios import Command
cmd = Command()
cmd.handle(idosos=5, dias=7)
"
```

### 8️⃣ Colete arquivos estáticos

```bash
python manage.py collectstatic --noinput
```

### 9️⃣ Inicie o servidor de desenvolvimento

```bash
python manage.py runserver
```

Acesse: **http://127.0.0.1:8000/**

---

## ⚙️ Configuração

### Credenciais Padrão

Após executar o script de build, as credenciais padrão são:

- **Usuário**: `admin`
- **Senha**: `Admin123!`

⚠️ **IMPORTANTE**: Altere essas credenciais imediatamente em produção!

### Configurações Importantes

#### `settings.py`

```python
# Modo Debug (Desative em produção)
DEBUG = False

# Hosts permitidos
ALLOWED_HOSTS = ['seu-dominio.com', 'www.seu-dominio.com']

# Banco de dados
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}

# Segurança em Produção
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

---

## 💻 Uso

### Painel Administrativo

Acesse: **http://127.0.0.1:8000/admin/**

- Gerencie usuários e permissões
- Visualize todos os dados do sistema
- Gere dados fictícios para testes

### Dashboard Principal

Acesse: **http://127.0.0.1:8000/dashboard/**

- Visualize métricas em tempo real
- Monitore alertas críticos
- Filtre dados por idoso específico
- Acompanhe gráficos interativos

### Registro Público

Acesse: **http://127.0.0.1:8000/registrar/idoso/**

- Cadastro aberto para novos idosos
- Requer aprovação administrativa
- Ideal para captação de novos usuários

---

## 📁 Estrutura do Projeto

```
monitoramento-idosos/
│
├── idosos_monitoramento/      # Configurações do projeto Django
│   ├── settings.py            # Configurações principais
│   ├── urls.py                # Rotas principais
│   └── wsgi.py                # Configuração WSGI
│
├── monitoramento/             # App principal
│   ├── models.py              # Modelos de dados
│   ├── views.py               # Views e lógica
│   ├── urls.py                # Rotas do app
│   ├── forms.py               # Formulários
│   ├── admin.py               # Configuração admin
│   ├── management/            # Comandos personalizados
│   │   └── commands/
│   │       └── gerar_dados_ficticios.py
│   └── migrations/            # Migrações do banco
│
├── api/                       # API REST
│   ├── views.py               # ViewSets da API
│   ├── serializers.py         # Serializadores
│   └── urls.py                # Rotas da API
│
├── templates/                 # Templates HTML
│   ├── base.html              # Template base
│   ├── monitoramento/         # Templates do app
│   └── registration/          # Templates de auth
│
├── static/                    # Arquivos estáticos
│   └── css/
│       └── mobile.css         # CSS customizado
│
├── staticfiles/               # Arquivos estáticos coletados
├── requirements.txt           # Dependências Python
├── manage.py                  # CLI do Django
├── build.sh                   # Script de build (Render)
├── gunicorn.conf.py           # Configuração Gunicorn
├── render.yaml                # Configuração Render
└── README.md                  # Este arquivo
```

---

## 🔌 API REST

### Base URL

```
http://127.0.0.1:8000/api/
```

### Autenticação

A API usa **Token Authentication** e **Session Authentication**.

#### Obter Token

```bash
POST /api-token-auth/
Content-Type: application/json

{
  "username": "admin",
  "password": "Admin123!"
}
```

#### Usar Token

```bash
Authorization: Token seu-token-aqui
```

### Endpoints Principais

#### Idosos

```bash
# Listar todos
GET /api/idosos/

# Obter um específico
GET /api/idosos/{id}/

# Criar novo
POST /api/idosos/
{
  "nome": "Maria Silva",
  "data_nascimento": "1950-05-15",
  "cpf": "123.456.789-00",
  ...
}

# Atualizar
PUT /api/idosos/{id}/

# Deletar
DELETE /api/idosos/{id}/

# Ativar idoso
POST /api/idosos/{id}/ativar/

# Receber dados de saúde
POST /api/idosos/{id}/receber_dados/
{
  "dispositivo_id": "DEVICE-0001",
  "frequencia_cardiaca": 75,
  "pressao_sistolica": 120,
  "pressao_diastolica": 80,
  "saturacao_oxigenio": 98.5,
  "temperatura": 36.5
}
```

#### Dispositivos

```bash
GET /api/dispositivos/
POST /api/dispositivos/
GET /api/dispositivos/{id}/
PUT /api/dispositivos/{id}/
DELETE /api/dispositivos/{id}/
```

#### Dados de Saúde

```bash
# Listar com filtros
GET /api/dados-saude/?idoso=1&start_date=2025-01-01&end_date=2025-12-31

GET /api/dados-saude/{id}/
POST /api/dados-saude/
```

#### Alertas

```bash
# Listar alertas
GET /api/alertas/?visualizado=false&nivel=critico

# Marcar como lido
POST /api/alertas/{id}/marcar_lido/

# Emergências (tempo real)
GET /api/alertas/emergencia/?idoso=1
```

### Exemplo de Integração (Python)

```python
import requests

# Configuração
BASE_URL = "http://127.0.0.1:8000/api"
TOKEN = "seu-token-aqui"
headers = {"Authorization": f"Token {TOKEN}"}

# Enviar dados de saúde
dados = {
    "dispositivo_id": "DEVICE-001",
    "frequencia_cardiaca": 78,
    "pressao_sistolica": 125,
    "pressao_diastolica": 82,
    "saturacao_oxigenio": 97.5,
    "temperatura": 36.8,
    "passos": 5000
}

response = requests.post(
    f"{BASE_URL}/idosos/1/receber_dados/",
    json=dados,
    headers=headers
)

print(response.json())
```

---

## 🌐 Deploy

### Deploy no Render.com

#### 1️⃣ Configuração Inicial

1. Crie uma conta no [Render.com](https://render.com)
2. Conecte seu repositório GitHub
3. Crie um **PostgreSQL Database**
4. Crie um **Web Service**

#### 2️⃣ Variáveis de Ambiente (Render Dashboard)

```env
SECRET_KEY=sua-chave-secreta-gerada-automaticamente
DEBUG=False
ALLOWED_HOSTS=*
PYTHON_VERSION=3.11.0
DATABASE_URL=postgresql://... (gerado automaticamente pelo Render)
```

#### 3️⃣ Comandos de Build

O arquivo `render.yaml` já está configurado, mas você também pode configurar manualmente:

**Build Command:**
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput
```

**Start Command:**
```bash
gunicorn idosos_monitoramento.wsgi:application
```

#### 4️⃣ Deploy Automático

Após o primeiro deploy, cada push para a branch `main` dispara um novo deploy automaticamente.

### Deploy Manual (Outros Servidores)

#### Ubuntu/Debian

```bash
# Instalar dependências
sudo apt update
sudo apt install python3.11 python3-pip python3-venv postgresql nginx

# Configurar PostgreSQL
sudo -u postgres createdb monitoramento_db
sudo -u postgres createuser monitoramento_user

# Clonar e configurar
git clone https://github.com/seu-usuario/projeto.git
cd projeto
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
nano .env  # Editar configurações

# Rodar migrações
python manage.py migrate
python manage.py collectstatic --noinput

# Configurar Gunicorn e Nginx
# (Ver documentação completa do Django)
```

---

## 🧪 Testes

### Executar Todos os Testes

```bash
python manage.py test
```

### Testes Específicos

```bash
# Testar models
python manage.py test monitoramento.tests.IdosoModelTest

# Testar views
python manage.py test monitoramento.tests.ViewsTest

# Testar API
python manage.py test monitoramento.tests.APITest
```

### Cobertura de Testes

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Gera relatório HTML
```

---

## 🤝 Contribuindo

Contribuições são muito bem-vindas! Siga estas etapas:

### 1️⃣ Fork o projeto

### 2️⃣ Crie uma branch para sua feature

```bash
git checkout -b feature/MinhaNovaFeature
```

### 3️⃣ Commit suas mudanças

```bash
git commit -m 'Adiciona nova funcionalidade X'
```

### 4️⃣ Push para a branch

```bash
git push origin feature/MinhaNovaFeature
```

### 5️⃣ Abra um Pull Request

### 📋 Diretrizes

- Siga o PEP 8 (Python)
- Adicione testes para novas funcionalidades
- Atualize a documentação quando necessário
- Use commits semânticos
- Mantenha o código limpo e bem comentado

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

```
MIT License

Copyright (c) 2025 Seu Nome

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 📞 Contato

**Desenvolvedor**: Seu Nome

- 📧 Email: seu-email@exemplo.com
- 🐙 GitHub: [@seu-usuario](https://github.com/seu-usuario)
- 💼 LinkedIn: [Seu Perfil](https://linkedin.com/in/seu-perfil)
- 🌐 Website: [seu-site.com](https://seu-site.com)

**Instituição**: IFSP Capivari

---

## 🙏 Agradecimentos

- [Django Project](https://www.djangoproject.com/)
- [Bootstrap Team](https://getbootstrap.com/)
- [Chart.js](https://www.chartjs.org/)
- [Font Awesome](https://fontawesome.com/)
- [Render.com](https://render.com/)
- IFSP Capivari - Professores e orientadores
- Comunidade Open Source

---

## 📊 Status do Projeto

![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)
![Versão](https://img.shields.io/badge/Versão-1.0.0-blue)
![Manutenção](https://img.shields.io/badge/Manutenção-Ativa-green)

---

## 🗺️ Roadmap

### ✅ Versão 1.0 (Atual)
- [x] Sistema de cadastro de idosos
- [x] Dashboard com gráficos
- [x] Sistema de alertas
- [x] API REST
- [x] Relatórios PDF/CSV
- [x] Interface responsiva

### 🚧 Versão 1.1 (Próxima)
- [ ] Notificações por email/SMS
- [ ] App mobile (React Native)
- [ ] Integração com smartwatches
- [ ] Chat entre responsáveis e cuidadores
- [ ] Histórico médico detalhado

### 🔮 Versão 2.0 (Futuro)
- [ ] Machine Learning para previsão de riscos
- [ ] Integração com sistemas de saúde (SUS)
- [ ] Telemedicina integrada
- [ ] Multi-idiomas
- [ ] White-label para instituições

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela no GitHub! ⭐**

Feito com ❤️ e ☕ por [Seu Nome]

</div>
