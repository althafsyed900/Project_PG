from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-pg/', views.add_pg, name='add_pg'),
    path('pg/<int:pg_id>/', views.pg_detail, name='pg_detail'),
    path('pg/<int:pg_id>/add-room/', views.add_room, name='add_room'),
    path('room/<int:room_id>/', views.room_detail, name='room_detail'),
    path('room/<int:room_id>/add-resident/', views.add_resident, name='add_resident'),
    path('pg/<int:pg_id>/edit/', views.edit_pg, name='edit_pg'),
    path('room/<int:room_id>/edit/', views.edit_room, name='edit_room'),
    path('resident/<int:resident_id>/edit/', views.edit_resident, name='edit_resident'),
    path('resident/<int:resident_id>/payments/', views.resident_payments, name='resident_payments'),
    path('resident/<int:resident_id>/payments/add/', views.add_payment, name='add_payment'),
    path('payment/<int:payment_id>/delete/', views.delete_payment, name='delete_payment'),
    path('pg/<int:pg_id>/delete/', views.delete_pg, name='delete_pg'),
    path('room/<int:room_id>/delete/', views.delete_room, name='delete_room'),
    path('resident/<int:resident_id>/delete/', views.delete_resident, name='delete_resident'),

    # QR Code paths
    path('room/<int:room_id>/qr/', views.room_qr_code, name='room_qr_code'),
    path('resident/<int:resident_id>/qr/', views.resident_qr_code, name='resident_qr_code'),
    path('pg/<int:pg_id>/rooms-qr/', views.pg_rooms_with_qr, name='pg_rooms_qr'),
    path('room/<int:room_id>/residents-qr/', views.room_residents_with_qr, name='room_residents_qr'),
    
    # Public QR form endpoints (can be accessed without login)
    path('qr/room/form/<int:pg_id>/', views.scan_qr_room_form, name='scan_qr_room_form'),
    path('qr/resident/form/<int:room_id>/', views.scan_qr_resident_form, name='scan_qr_resident_form'),
]
