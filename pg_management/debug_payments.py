import os, sys, traceback
os.environ.setdefault('DJANGO_SETTINGS_MODULE','pg_management.settings')
import django
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from pgapp.models import PG, Room, Resident, Payment

c = Client()
try:
    # ensure testuser exists
    if not User.objects.filter(username='testuser').exists():
        User.objects.create_superuser('testuser','test@example.com','testpass')
    # login
    login_resp = c.post('/accounts/login/', {'username':'testuser','password':'testpass'})
    print('login status:', login_resp.status_code)

    # ensure a resident exists
    if not PG.objects.exists():
        pg = PG.objects.create(name='Demo PG', address='Address')
        room = Room.objects.create(pg=pg, room_number='101', capacity=3)
        r = Resident.objects.create(room=room, name='Alice', age=25)
    else:
        r = Resident.objects.first()

    # request payments page
    url = f'/resident/{r.id}/payments/'
    resp = c.get(url)
    print('GET', url, '=>', resp.status_code)
    content = resp.content.decode('utf-8', errors='replace')
    print('--- PAGE START ---')
    print(content[:4000])
    print('--- PAGE END ---')

except Exception:
    traceback.print_exc()
    sys.exit(1)
