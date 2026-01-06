from django.db import models

# Create your models here.


class Room(models.Model):
    room_number=models.IntegerField()
    capacity=models.IntegerField()
    price_per_night = models.DecimalField(max_digits=10,decimal_places=2)
    description =models.TextField()
    is_available = models.BooleanField(default=True)
    included_services =models.TextField()
    main_image= models.ImageField(upload_to='room/main/',null=True,blank=True)


class RoomImage(models.Model):
    room=models.ForeignKey(Room,related_name='images',on_delete=models.CASCADE)
    image=models.ImageField(upload_to='rooms/gallery/',)