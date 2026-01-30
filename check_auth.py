import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pg_management.settings')
django.setup()
from django.test import Client
c = Client()
resp = c.get('/')
print('Home status (not logged):', resp.status_code, resp['Location'] if resp.status_code in (301,302) else '')
# login attempt
from django.contrib.auth.models import User
if not User.objects.filter(username='testuser').exists():
    User.objects.create_superuser('testuser','test@example.com','testpass')
resp = c.post('/accounts/login/', {'username':'testuser','password':'testpass'})
print('Login post status:', resp.status_code)
resp2 = c.get('/')
print('Home status (after login):', resp2.status_code)
