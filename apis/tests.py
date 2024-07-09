from django.test import TestCase
from .models import Item
from django.utils import timezone
import datetime


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
