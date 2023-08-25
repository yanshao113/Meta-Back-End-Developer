from django.test import TestCase
from restaurant.models import Menu

class MenuViewTest(TestCase):

    def setUp(self):
        self.dish = Menu.objects.create(title='test',price=2,inventory=1)

    def test_getall(self):
        dish = Menu.objects.get(title='test')
        self.assertEqual(dish.status_code,200)
        self.assertEqual(dish.inventory,1)
        self.assertEqual(dish.price,2)
