@echo off
echo ======================================
echo CONFIGURACAO LOCAL - MONITORAMENTO IDOSOS
echo ======================================

echo [1/8] Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 goto erro

echo [2/8] Criando pasta static...
mkdir static 2>nul
echo. > static/.gitkeep

echo [3/8] Rodando migracoes...
python manage.py makemigrations
python manage.py migrate
if errorlevel 1 goto erro

echo [4/8] Criando superusuario padrao...
echo from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@local.com', 'admin123') | python manage.py shell

echo [5/8] Populando banco de demonstracao...
python manage.py populate_demo
if errorlevel 1 goto erro

echo [6/8] Coletando arquivos estaticos...
python manage.py collectstatic --noinput
if errorlevel 1 goto erro

echo [7/8] Iniciando servidor de desenvolvimento...
echo ======================================
echo ✅ TUDO PRONTO!
echo ======================================
echo Acesse: http://127.0.0.1:8000/
echo Admin: admin / admin123
echo API: http://127.0.0.1:8000/api/
echo ======================================
python manage.py runserver 0.0.0.0:8000
goto fim

:erro
echo ❌ ERRO NA EXECUCAO! Verifique as mensagens acima.
pause
exit /b 1

:fim