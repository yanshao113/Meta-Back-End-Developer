from django.test import TestCase
from restaurant.models import Booking,Menu
from datetime import datetime

class MenuItemTest(TestCase):

    def test_get_item(self):
        item= Menu.objects.create(title="IceCream", price=80, inventory=100)
        self.assertEqual(item.title, 'IceCream')
        self.assertEqual(item.price, 80.00)
        self.assertEqual(item.inventory, 100)


class BookingTest(TestCase):
    def test_get_item(self):
        record = Booking.objects.create(name="Ada", booking_date=datetime(2023,8,25,11,0),no_of_guests=2)
        self.assertEqual(record.name,"Ada")
        self.assertEqual(record.no_of_guests,2)
