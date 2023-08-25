from django.test import TestCase
from restaurant.models import Booking,Menu
from datetime import datetime

class MenuItemTest(TestCase):
    def test_get_item(self):
        item = Menu.objects.create(title="IceCream", price=80, inventory=100)
        self.assertEqual(item, "IceCream : 80")


class BookingTest(TestCase):
    def test_get_item(self):
        record = Booking.objects.create(name="Ada", booking_date=datetime(2023,8,25,11,0),no_of_guests=2)
        self.assertEqual(record,"Ada : 2 (guest/guests) on 2023-08-25 11:00:00")
