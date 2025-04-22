#!/usr/bin/env bash
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Moverse a la carpeta del proyecto Django
# cd proyecto_django

# Recoger archivos estáticos (solo si usas templates/admin)
python manage.py collectstatic --no-input

# Aplicar migraciones
python manage.py migrate
