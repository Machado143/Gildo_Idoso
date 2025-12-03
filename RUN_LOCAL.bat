@echo off
REM Pasta static
if not exist "static" mkdir static

REM Instalar pacotes
pip install -r requirements.txt

REM Migrações
python manage.py makemigrations
python manage.py migrate

REM Criar superuser (se não existir)
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@local.com', 'admin123')"

REM Popular dados demo
python manage.py populate_demo

REM Iniciar servidor
python manage.py runserver 0.0.0.0:8000