from rest_framework import serializers
from .models import Category,MenuItem,Cart,Order,OrderItem
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.models import User
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','title']

class MenuItemSerializer(serializers.ModelSerializer):
    category_id= serializers.IntegerField(write_only=True)
    category=serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    class Meta:
        model=MenuItem
        fields=['id','title','price','featured','category','category_id']
        extra_kwargs={'price':{'min_value':2},'category':{'read_only':True}}

class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    validators = [UniqueTogetherValidator(
        queryset=Cart.objects.all(),
        fields=['user', 'menuitem_id']
    )
]
    class Meta:
        model=Cart
        fields=['user','menuitem','quantity','unit_price','price']
        extra_kwargs={'price':{'min_value':2,'read_only':True},'quantity':{'min_value':0}}

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model=Order
        fields=['id','user','delivery_crew','status','total','date']

class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model=OrderItem
        fields=['order','menuitem','quantity','unit_price','price']


