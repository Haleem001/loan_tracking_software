import os
from django.core.wsgi import get_wsgi_application

# Set your settings module; replace 'myproject.settings' with your actual settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loan_tracker.settings')

# Create the WSGI application
app = get_wsgi_application()

