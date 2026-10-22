from django.test import TestCase, Client
from django.urls import reverse
from app.models import Item

class ViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_health_check(self):
        response = self.client.get(reverse('health_check'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'ok')

    def test_item_list_view(self):
        response = self.client.get(reverse('app:item_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django 5 + Tailwind + PostgreSQL")

    def test_item_create_view(self):
        response = self.client.post(reverse('app:item_create'), {
            'title': 'Test Item',
            'description': 'Test Description',
            'priority': 'medium'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().title, 'Test Item')

    def test_item_toggle_view(self):
        item = Item.objects.create(title="Toggle Test")
        self.assertFalse(item.is_completed)
        response = self.client.post(reverse('app:item_toggle', args=[item.pk]))
        self.assertEqual(response.status_code, 302)
        item.refresh_from_db()
        self.assertTrue(item.is_completed)
