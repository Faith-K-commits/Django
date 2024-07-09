from django.test import TestCase
from .models import Item
from django.utils import timezone
import datetime
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class ItemAPIGETTestCase(TestCase):
    def setUp(self):
        self.test_item = Item.objects.create(name='Test Item')

    def test_name_field(self):
        self.assertEqual(self.test_item.name, 'Test Item')

    def test_created_field(self):
        self.assertTrue(isinstance(self.test_item.created, datetime.datetime))
        self.assertTrue(self.test_item.created <= timezone.now())

    def test_updated_field(self):
        self.assertTrue(isinstance(self.test_item.updated, datetime.datetime))
        self.assertTrue(self.test_item.updated <= timezone.now())


class ItemAPIPOSTTestCase(APITestCase):
    def test_create_item(self):
        url = reverse('apis:post_items')
        data = {
            'name': 'Test Item',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get().name, 'Test Item')

    def test_post_item_invalid_data(self):
        url = reverse('apis:post_items')
        data = {
            'name': '',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Item.objects.count(), 0)
