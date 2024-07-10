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


class ItemAPIPATCHTestCase(APITestCase):
    def setUp(self):
        self.item = Item.objects.create(name='Initial Item')

    def test_patch_item_success(self):
        url = reverse('apis:patch_item', args=[self.item.id])
        data = {'name': 'Updated Item'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Item.objects.get(pk=self.item.id).name, 'Updated Item')

    def test_patch_item_not_found(self):
        url = reverse('apis:patch_item', args=[999])  # Non-existent item ID
        data = {'name': 'Updated Item'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'error': 'Item not found.'})

    def test_patch_item_invalid_data(self):
        url = reverse('apis:patch_item', args=[self.item.id])
        data = {'name': ''}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)


class ItemAPIDeleteTestCase(APITestCase):
    def setUp(self):
        self.item = Item.objects.create(name='Item to be deleted')

    def test_delete_item_success(self):
        url = reverse('apis:delete_items', args=[self.item.id])  
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)

    def test_delete_item_not_found(self):
        url = reverse('apis:delete_items', args=[999])  # Non-existent item ID
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'error': 'Item not found.'})
