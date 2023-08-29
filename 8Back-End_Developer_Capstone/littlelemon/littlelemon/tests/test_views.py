from django.test import TestCase,Client
from rest_framework import status
from rest_framework.test import APIClient
from restaurant.models import Menu
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from decimal import *


class MenuViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_getall(self):
        url=reverse('menu')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)


class SingleMenuItemViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.menu_item = Menu.objects.create(
            title="test",
            price="12.00",
            inventory=5
        )
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)

    def test_get_single_menu_item(self):
        url = reverse('menu_item', kwargs={'pk': self.menu_item.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            "id": self.menu_item.pk,
            "title": "test",
            "price": "12.00",
            "inventory": 5
        }
        self.assertEqual(response.data, expected_data)

    def test_update_single_menu_item(self):
        url = reverse('menu_item', kwargs={'pk': self.menu_item.pk})
        data = {
            "title": "Updated Salad",
            "price": "14.00",
            "inventory": 8
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.title, 'Updated Salad')
        self.assertEqual(self.menu_item.price, Decimal(14))
        self.assertEqual(self.menu_item.inventory, 8)

    def test_delete_single_menu_item(self):
        url = reverse('menu_item', kwargs={'pk': self.menu_item.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Menu.objects.count(), 0)
