from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PG, Room, Resident, Payment
from django.db.models import Sum
from .forms import PGForm, RoomForm, ResidentForm, PaymentForm
from .qr_utils import generate_room_qr_url, generate_resident_qr_url
from django.http import JsonResponse
from django.urls import reverse
import json

@login_required
def home(request):
    pgs = PG.objects.all()
    return render(request, 'home.html', {'pgs': pgs})

@login_required
def add_pg(request):
    if request.method == 'POST':
        form = PGForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PGForm()
    return render(request, 'add_pg.html', {'form': form})

@login_required
def pg_detail(request, pg_id):
    pg = get_object_or_404(PG, id=pg_id)
    rooms = Room.objects.filter(pg=pg)
    return render(request, 'pg_detail.html', {'pg': pg, 'rooms': rooms})
@login_required
def add_room(request, pg_id):
    pg = get_object_or_404(PG, id=pg_id)

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.pg = pg
            room.save()
            return redirect('room_qr_code', room_id=room.id)
    else:
        form = RoomForm()

    return render(request, 'add_room.html', {'form': form, 'pg': pg})

@login_required
def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    residents = Resident.objects.filter(room=room)
    return render(request, 'room_detail.html', {'room': room, 'residents': residents})


@login_required
def add_resident(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        form = ResidentForm(request.POST, request.FILES)
        if form.is_valid():
            resident = form.save(commit=False)
            resident.room = room
            resident.save()
            return redirect('resident_qr_code', resident_id=resident.id)
    else:
        form = ResidentForm()

    return render(request, 'add_resident.html', {'form': form, 'room': room})


@login_required
def delete_pg(request, pg_id):
    pg = get_object_or_404(PG, id=pg_id)
    if request.method == 'POST':
        pg.delete()
        return redirect('home')
    return render(request, 'delete_confirm.html', {'type': 'PG', 'object': pg})

@login_required
def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        room.delete()
        return redirect('pg_detail', pg_id=room.pg.id)
    return render(request, 'delete_confirm.html', {'type': 'Room', 'object': room})

@login_required
def edit_pg(request, pg_id):
    pg = get_object_or_404(PG, id=pg_id)
    if request.method == 'POST':
        form = PGForm(request.POST, instance=pg)
        if form.is_valid():
            form.save()
            return redirect('pg_detail', pg_id=pg.id)
    else:
        form = PGForm(instance=pg)
    return render(request, 'edit_pg.html', {'form': form, 'pg': pg})

@login_required
def edit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('room_detail', room_id=room.id)
    else:
        form = RoomForm(instance=room)
    return render(request, 'edit_room.html', {'form': form, 'room': room})

@login_required
def edit_resident(request, resident_id):
    resident = get_object_or_404(Resident, id=resident_id)
    if request.method == 'POST':
        form = ResidentForm(request.POST, request.FILES, instance=resident)
        if form.is_valid():
            form.save()
            return redirect('room_detail', room_id=resident.room.id)
    else:
        form = ResidentForm(instance=resident)
    return render(request, 'edit_resident.html', {'form': form, 'resident': resident})


@login_required
def resident_payments(request, resident_id):
    resident = get_object_or_404(Resident, id=resident_id)
    payments = Payment.objects.filter(resident=resident).order_by('-payment_date')
    total = payments.aggregate(total=Sum('amount'))['total']
    return render(request, 'payments_list.html', {'resident': resident, 'payments': payments, 'total_amount': total})


@login_required
def add_payment(request, resident_id):
    resident = get_object_or_404(Resident, id=resident_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.resident = resident
            payment.save()
            return redirect('resident_payments', resident_id=resident.id)
    else:
        form = PaymentForm()
    return render(request, 'add_payment.html', {'form': form, 'resident': resident})


@login_required
def delete_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    resident = payment.resident
    if request.method == 'POST':
        payment.delete()
        return redirect('resident_payments', resident_id=resident.id)
    return render(request, 'delete_confirm.html', {'type': 'Payment', 'object': payment})

@login_required
def delete_resident(request, resident_id):
    resident = get_object_or_404(Resident, id=resident_id)
    if request.method == 'POST':
        resident.delete()
        return redirect('room_detail', room_id=resident.room.id)
    return render(request, 'delete_confirm.html', {'type': 'Resident', 'object': resident})


# QR Code Views
@login_required
def room_qr_code(request, room_id):
    """Generate QR code for room form with scannable URL"""
    room = get_object_or_404(Room, id=room_id)
    # Generate URL for the form that can be scanned
    form_url = request.build_absolute_uri(reverse('scan_qr_room_form', kwargs={'pg_id': room.pg.id}))
    qr_image = generate_room_qr_url(form_url)
    
    return render(request, 'room_qr_code.html', {
        'room': room,
        'qr_image': qr_image,
        'form_url': form_url
    })


@login_required
def resident_qr_code(request, resident_id):
    """Generate QR code for resident form with scannable URL"""
    resident = get_object_or_404(Resident, id=resident_id)
    # Generate URL for the form that can be scanned
    form_url = request.build_absolute_uri(reverse('scan_qr_resident_form', kwargs={'room_id': resident.room.id}))
    qr_image = generate_resident_qr_url(form_url)
    
    return render(request, 'resident_qr_code.html', {
        'resident': resident,
        'qr_image': qr_image,
        'form_url': form_url
    })


def scan_qr_room_form(request, pg_id):
    """Public form page for adding room via QR code"""
    pg = get_object_or_404(PG, id=pg_id)
    
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.pg = pg
            room.save()
            return render(request, 'qr_room_success.html', {
                'room': room,
                'pg': pg,
                'message': f'Room {room.room_number} added successfully!'
            })
    else:
        form = RoomForm()
    
    return render(request, 'scan_qr_room_form.html', {
        'form': form,
        'pg': pg
    })


def scan_qr_resident_form(request, room_id):
    """Public form page for adding resident via QR code"""
    room = get_object_or_404(Room, id=room_id)
    
    if request.method == 'POST':
        form = ResidentForm(request.POST, request.FILES)
        if form.is_valid():
            resident = form.save(commit=False)
            resident.room = room
            resident.save()
            return render(request, 'qr_resident_success.html', {
                'resident': resident,
                'room': room,
                'message': f'Resident {resident.name} added successfully!'
            })
    else:
        form = ResidentForm()
    
    return render(request, 'scan_qr_resident_form.html', {
        'form': form,
        'room': room
    })


@login_required
def pg_rooms_with_qr(request, pg_id):
    """Display all rooms in a PG with their QR codes"""
    pg = get_object_or_404(PG, id=pg_id)
    rooms = Room.objects.filter(pg=pg)
    
    rooms_with_qr = []
    for room in rooms:
        form_url = request.build_absolute_uri(reverse('scan_qr_room_form', kwargs={'pg_id': pg.id}))
        qr_image = generate_room_qr_url(form_url)
        rooms_with_qr.append({
            'room': room,
            'qr_image': qr_image,
            'form_url': form_url
        })
    
    return render(request, 'pg_rooms_qr.html', {
        'pg': pg,
        'rooms': rooms_with_qr
    })


@login_required
def room_residents_with_qr(request, room_id):
    """Display all residents in a room with their QR codes"""
    room = get_object_or_404(Room, id=room_id)
    residents = Resident.objects.filter(room=room)
    
    residents_with_qr = []
    for resident in residents:
        form_url = request.build_absolute_uri(reverse('scan_qr_resident_form', kwargs={'room_id': room.id}))
        qr_image = generate_resident_qr_url(form_url)
        residents_with_qr.append({
            'resident': resident,
            'qr_image': qr_image,
            'form_url': form_url
        })
    
    return render(request, 'room_residents_qr.html', {
        'room': room,
        'residents': residents_with_qr
    })
