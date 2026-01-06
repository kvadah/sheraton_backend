from django.db import models

from accounts.models import User

# Create your models here.


class Room(models.Model):
    room_number = models.IntegerField()
    capacity = models.IntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    included_services = models.TextField()
    main_image = models.ImageField(
        upload_to='room/main/', null=True, blank=True)


class RoomImage(models.Model):
    room = models.ForeignKey(
        Room, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='rooms/gallery/',)


class Booking(models.Model):
    BOOKING_STATUS = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    )
    user = models.ForeignKey(
        User, related_name='books', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=BOOKING_STATUS, default='pending')
    booked_at = models.DateTimeField(auto_now_add=True)
