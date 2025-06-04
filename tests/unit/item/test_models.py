from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from item.models import Category, Comment, Item, Purchase


class TestModels(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Create test category
        self.category = Category.objects.create(name="Test Category")

        # Create test comment
        self.comment = Comment.objects.create(
            user=self.user,
            description="This is a test comment.",
            created_at=timezone.now(),
        )

        # Create test item
        self.item = Item.objects.create(
            category=self.category,
            name="Test Item",
            description="Test item description.",
            price=19.99,
            gender="M",  # Using 'M' for Man as per the choices
        )
        self.item.comments.add(self.comment)

        # Create test purchase
        self.purchase = Purchase.objects.create(
            user=self.user, telegram="test_telegram_id", price=39.99
        )
        self.purchase.items.add(self.item)

    def test_category_creation(self):
        category = Category.objects.get(id=self.category.id)
        self.assertEqual(category.name, "Test Category")
        self.assertEqual(str(category), "Test Category")

    def test_comment_creation(self):
        comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(comment.description, "This is a test comment.")
        self.assertEqual(comment.user, self.user)
        self.assertEqual(str(comment), "This is a test comment.")

    def test_item_creation(self):
        item = Item.objects.get(id=self.item.id)
        self.assertEqual(item.name, "Test Item")
        self.assertEqual(item.price, 19.99)
        self.assertEqual(item.gender, "M")  # Man as per the gender_choice dict
        self.assertEqual(item.category, self.category)
        self.assertEqual(str(item), "Test Item")

    def test_item_comments(self):
        item = Item.objects.get(id=self.item.id)
        self.assertIn(self.comment, item.comments.all())

    def test_purchase_creation(self):
        purchase = Purchase.objects.get(id=self.purchase.id)
        self.assertEqual(purchase.telegram, "test_telegram_id")
        self.assertEqual(purchase.price, 39.99)
        self.assertEqual(purchase.user, self.user)
        self.assertIn(self.item, purchase.items.all())

    def test_purchase_item_relation(self):
        purchase = Purchase.objects.get(id=self.purchase.id)
        self.assertIn(self.item, purchase.items.all())

    def test_purchase_user_relation(self):
        purchase = Purchase.objects.get(id=self.purchase.id)
        self.assertEqual(purchase.user, self.user)
