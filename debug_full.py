import os, sys, traceback
os.environ.setdefault('DJANGO_SETTINGS_MODULE','pg_management.settings')
import django
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from pgapp.models import PG, Room, Resident, Payment

c = Client()
try:
    print('--- Ensuring test user exists')
    if not User.objects.filter(username='testuser').exists():
        User.objects.create_superuser('testuser','test@example.com','testpass')
        print('created testuser')
    else:
        print('testuser exists')

    # login
    login_resp = c.post('/accounts/login/', {'username':'testuser','password':'testpass'})
    print('login status:', login_resp.status_code)

    # ensure sample data
    if not PG.objects.exists():
        pg = PG.objects.create(name='Demo PG', address='Address')
        room = Room.objects.create(pg=pg, room_number='101', capacity=3)
        r = Resident.objects.create(room=room, name='Alice', age=25)
        print('created sample PG, room, resident')
    else:
        pg = PG.objects.first()
        room = Room.objects.filter(pg=pg).first()
        if not room:
            room = Room.objects.create(pg=pg, room_number='101', capacity=3)
        r = Resident.objects.filter(room=room).first() or Resident.objects.create(room=room, name='Alice', age=25)
        print('sample data exists')

    urls = [
        ('home','/'),
        ('pg_detail', f'/pg/{pg.id}/'),
        ('room_detail', f'/room/{room.id}/'),
        ('add_resident', f'/room/{room.id}/add-resident/'),
        ('payments', f'/resident/{r.id}/payments/'),
        ('add_payment', f'/resident/{r.id}/payments/add/'),
    ]

    for name, url in urls:
        resp = c.get(url)
        print(f'GET {name} {url} =>', resp.status_code)
        if resp.status_code >= 500:
            print('--- Error page snippet ---')
            print(resp.content.decode('utf-8','replace')[:2000])
            print('--- End snippet ---')

    # create a payment
    Payment.objects.create(resident=r, amount=1500, month='Jan 2026', payment_date='2026-01-05')
    resp = c.get(f'/resident/{r.id}/payments/')
    print('after add payment, payments page status', resp.status_code)
    print('payments page contains Total?', b'Total:' in resp.content)

    print('Debug completed successfully')

except Exception:
    traceback.print_exc()
    sys.exit(1)
