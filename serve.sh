#!/bin/bash

# Navigate to the project directory
cd ~/GRAMbackend || exit

# Activate the virtual environment
source venv/bin/activate

# Start Gunicorn with wsgi.py as the WSGI application
gunicorn --daemon \
         --workers 3 \
         --bind 0.0.0.0:8080 \
         --access-logfile access.log \
         --error-logfile error.log \
         wsgi:app