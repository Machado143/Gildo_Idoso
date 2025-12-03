#!/bin/bash
# ==========================================
# BUILD SCRIPT - RENDER.COM
# Otimizado para PostgreSQL
# ==========================================

set -e  # Para na primeira falha

echo "🚀 Iniciando build no Render..."

# 1. Instalar dependências
echo "📦 Instalando dependências Python..."
pip install --upgrade pip
pip install -r requirements.txt

# 2. Coletar arquivos estáticos
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear

# 3. Rodar migrações
echo "🗄️ Aplicando migrações do banco de dados..."
python manage.py migrate --noinput

# 4. Criar superusuário (se não existir)
echo "👤 Verificando superusuário..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@monitoramento.com',
        password='Admin123!'
    )
    print('✅ Superusuário criado: admin / Admin123!')
else:
    print('ℹ️ Superusuário já existe')
EOF

# 5. Popular dados demo (OPCIONAL - comentar em produção)
echo "🎲 Populando dados de demonstração..."
python manage.py populate_demo || echo "⚠️ Dados demo já existem ou comando falhou (OK)"

echo "✅ Build concluído com sucesso!"
echo "🌐 Aplicação pronta para deploy!"