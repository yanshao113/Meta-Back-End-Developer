from rest_framework import serializers
from .models import Booking,Menu
from django.contrib.auth.models import User

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model= Menu
        fields=['id','title','price','inventory']
        extra_kwargs={
            'price':{"min_value":1},
            'inventory':{"min_value":0},
        }

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Booking
        fields='__all__'
        extra_kwargs={
            'no_of_guests':{"min_value":1},
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['url','username','email','groups']