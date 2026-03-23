#!/bin/bash
# Setup script for PRIME Backend - macOS/Linux

echo "Creating Python virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate

echo "Creating superuser..."
echo "Please enter superuser details:"
python manage.py createsuperuser

echo ""
echo "========================================"
echo "Setup complete!"
echo "========================================"
echo ""
echo "To start the development server, run:"
echo "python manage.py runserver"
echo ""
echo "To load sample data, run:"
echo "python manage.py load_sample_data"
echo ""
echo "Admin panel: http://localhost:8000/admin/"
echo "API: http://localhost:8000/api/"
echo ""
