#!/bin/bash
set -e

echo "Aguardando o banco de dados..."
while ! python -c "
import os, socket
host = os.environ.get('POSTGRES_HOST', 'db')
port = int(os.environ.get('POSTGRES_PORT', 5432))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(1)
s.connect((host, port))
s.close()
" 2>/dev/null; do
    echo "Banco ainda não está pronto... aguardando 1s"
    sleep 1
done

echo "Banco pronto! Rodando migrations..."
python manage.py migrate --noinput

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "Iniciando Gunicorn..."
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 2
