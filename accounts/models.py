from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('guest','Guest'),
        ('admin','Admin')
    )
    email =models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    role= models.CharField(max_length=10,choices=ROLE_CHOICES,default='guest')
    



    def __str__(self):
        return self.name
    