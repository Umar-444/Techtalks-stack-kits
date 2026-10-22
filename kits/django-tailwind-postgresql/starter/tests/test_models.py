from django.test import TestCase
from app.models import Item

class ItemModelTest(TestCase):
    def test_create_item(self):
        item = Item.objects.create(
            title="Setup PostgreSQL Indexing",
            description="Add composite index on is_completed and created_at",
            priority="high"
        )
        self.assertEqual(item.title, "Setup PostgreSQL Indexing")
        self.assertFalse(item.is_completed)
        self.assertEqual(str(item), "Setup PostgreSQL Indexing")
