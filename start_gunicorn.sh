#!/bin/bash
source /home/pi/GRAMbackend/venv/bin/activate
exec /home/pi/GRAMbackend/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8080 wsgi:app