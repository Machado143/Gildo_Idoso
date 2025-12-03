@echo off
REM Script sem celery para rodar imediatamente

echo Criando pasta static...
mkdir static 2>nul
echo. > static/.gitkeep

echo Rodando migrações...
python manage.py makemigrations monitoramento
python manage.py migrate

echo Criando superuser...
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@local.com', 'admin123')"

echo Populando dados demo...
python manage.py populate_demo

echo Iniciando servidor...
python manage.py runserver 0.0.0.0:8000