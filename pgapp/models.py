from django.db import models

class PG(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name

class Room(models.Model):
    pg = models.ForeignKey(PG, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    capacity = models.IntegerField()

    def __str__(self):
        return f"Room {self.room_number}"

class Resident(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, default='Not specified', blank=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    joining_date = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return self.name

class Payment(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.CharField(max_length=20)
    payment_date = models.DateField()
