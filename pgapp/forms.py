from django import forms
from .models import PG
from .models import Room
from .models import Resident
from .models import Payment

class PGForm(forms.ModelForm):
    class Meta:
        model = PG
        fields = ['name', 'address']

class RoomForm(forms.ModelForm):
    ROOM_CHOICES = [
        ('G1', 'G1'), ('G2', 'G2'), ('G3', 'G3'), ('G4', 'G4'), ('G5', 'G5'), ('G6', 'G6'), ('G7', 'G7'), ('G8', 'G8'), ('G9', 'G9'), ('G10', 'G10'),
        ('101', '101'), ('102', '102'), ('103', '103'), ('104', '104'), ('105', '105'), ('106', '106'), ('107', '107'), ('108', '108'), ('109', '109'), ('110', '110'),
        ('201', '201'), ('202', '202'), ('203', '203'), ('204', '204'), ('205', '205'), ('206', '206'), ('207', '207'), ('208', '208'), ('209', '209'), ('210', '210'),
        ('301', '301'), ('302', '302'), ('303', '303'), ('304', '304'), ('305', '305'), ('306', '306'), ('307', '307'), ('308', '308'), ('309', '309'), ('310', '310'),
        ('401', '401'), ('402', '402'), ('403', '403'), ('404', '404'), ('405', '405'), ('406', '406'), ('407', '407'), ('408', '408'), ('409', '409'), ('410', '410'),
        ('501', '501'), ('502', '502'), ('503', '503'), ('504', '504'), ('505', '505'), ('506', '506'), ('507', '507'), ('508', '508'), ('509', '509'), ('510', '510'),
    ]
    CAPACITY_CHOICES = [
        (3, '3 Sharing'),
        (5, '5 Sharing'),
    ]
    room_number = forms.ChoiceField(choices=ROOM_CHOICES)
    capacity = forms.ChoiceField(choices=CAPACITY_CHOICES)
    
    class Meta:
        model = Room
        fields = ['room_number', 'capacity']

class ResidentForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
        ('Not specified', 'Not specified'),
    ]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=False)
    joining_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':3}))
    mobile_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'type': 'tel', 'placeholder': '+91 XXXXX XXXXX'}))
    
    class Meta:
        model = Resident
        fields = ['name', 'age', 'gender', 'joining_date', 'address', 'mobile_number', 'photo']


class PaymentForm(forms.ModelForm):
    payment_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Payment
        fields = ['amount', 'month', 'payment_date']