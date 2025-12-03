# run_now.ps1
Write-Host "=== INICIANDO SISTEMA DE MONITORAMENTO ===" -ForegroundColor Cyan

# Passo 1: Instalar dependências
Write-Host "Instalando dependências..." -ForegroundColor Yellow
pip install -r requirements.txt

# Passo 2: Migrações
Write-Host "Rodando migrações..." -ForegroundColor Yellow
python manage.py makemigrations monitoramento
python manage.py migrate

# Passo 3: Criar superuser
Write-Host "Criando superuser..." -ForegroundColor Yellow
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@local.com', 'admin123')"

# Passo 4: Popular dados
Write-Host "Populando dados de demonstração..." -ForegroundColor Yellow
python manage.py populate_demo

# Passo 5: Iniciar servidor
Write-Host "Iniciando servidor..." -ForegroundColor Green
python manage.py runserver 0.0.0.0:8000