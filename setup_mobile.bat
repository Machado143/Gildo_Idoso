@echo off
echo === OTIMIZANDO PARA MOBILE ===

echo Criando pastas...
mkdir static\images 2>nul
mkdir static\css 2>nul
mkdir static\js 2>nul

echo Baixando ícones padrão...
echo (Substitua estes arquivos manualmente depois)
echo. > static\images\favicon.ico
echo. > static\images\apple-touch-icon.png
echo. > static\images\icon-192.png
echo. > static\images\icon-512.png

echo ✅ Mobile setup completo!
echo Próximos passos:
echo 1. Gere ícones em: https://favicon.io/
echo 2. Substitua os arquivos em static/images/
echo 3. Faça commit e deploy