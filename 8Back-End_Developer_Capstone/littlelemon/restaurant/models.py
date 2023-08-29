from django.db import models
from datetime import datetime
# Create your models here.


class Booking(models.Model):
    name = models.CharField(max_length=255)
    booking_date = models.DateField(auto_now=True)
    no_of_guests = models.SmallIntegerField(default=6)

    def __str__(self):
        return f'{self.name} : {str(self.no_of_guests)} (guest/guests) on {str(self.booking_date)}'


class Menu(models.Model):
   title= models.CharField(max_length=255)
   price = models.DecimalField(max_digits=10,decimal_places=2,db_index=True)
   inventory=models.SmallIntegerField(default=5)

   def __str__(self):
      return f'{self.title} : {str(self.price)}'