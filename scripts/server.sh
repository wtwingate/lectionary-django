#! /bin/bash

# Use development settings
export DJANGO_SETTINGS_MODULE=website.settings_dev

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Start development server
python manage.py runserver
