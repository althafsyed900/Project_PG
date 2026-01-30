from django.contrib import admin
from .models import PG, Room, Resident, Payment

admin.site.register(PG)
admin.site.register(Room)
admin.site.register(Resident)
admin.site.register(Payment)
