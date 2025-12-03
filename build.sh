#!/bin/bash

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput

echo "👤 Verificando superusuário..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@paidoverde.com', 'Admin123!')
    print('✅ Superusuário criado: admin / Admin123!')
else:
    print('ℹ️ Superusuário já existe')
EOF

echo "✅ Build concluído com sucesso!"