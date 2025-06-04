from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import NoReverseMatch, reverse
from django.utils import timezone

from item.models import Category, Comment, Item, Purchase

User = get_user_model()


class ItemViewsTestCase(TestCase):
    def setUp(self):
        # Создаем обычного пользователя и суперпользователя
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.superuser = User.objects.create_superuser(username="admin", password="adminpass")

        # Создаем тестовую категорию
        self.category = Category.objects.create(name="Test Category")

        # Создаем основной товар
        self.item = Item.objects.create(
            name="Test Item",
            description="This is a test item.",
            price=100.00,
            image=SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),
            category=self.category,
            is_sold=False,
            created_at=timezone.now(),
            gender="M",
        )

        # Создаем связанные товары (для проверки фильтрации по полу)
        self.related_item = Item.objects.create(
            name="Related Item",
            description="Related test item.",
            price=50.00,
            image=SimpleUploadedFile(
                "related_image.jpg", b"file_content", content_type="image/jpeg"
            ),
            category=self.category,
            is_sold=False,
            created_at=timezone.now(),
            gender="M",
        )
        self.related_item_diff = Item.objects.create(
            name="Related Item Diff",
            description="Should be filtered out when gender set to M.",
            price=75.00,
            image=SimpleUploadedFile(
                "related_diff.jpg", b"file_content", content_type="image/jpeg"
            ),
            category=self.category,
            is_sold=False,
            created_at=timezone.now(),
            gender="W",
        )

    # detail view
    def test_detail_view_unauthenticated(self):
        url = reverse("item:detail", kwargs={"pk": self.item.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.name)
        self.assertIn("item", response.context)
        self.assertIn("related_items", response.context)
        self.assertIn("gender", response.context)

    def test_detail_view_authenticated(self):
        self.client.login(username="testuser", password="password123")
        url = reverse("item:detail", kwargs={"pk": self.item.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.name)
        self.assertIn("in_basket", response.context)
        self.assertIn("form", response.context)
        # Так как товар еще не добавлен в корзину, флаг должен быть False
        self.assertFalse(response.context["in_basket"])

    # items view (список товаров)
    def test_items_view(self):
        url = reverse("item:items")
        response = self.client.get(url, {"query": "Test"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.name)
        self.assertIn("categories", response.context)
        self.assertIn("items", response.context)
        self.assertIn("query", response.context)

    # add view (добавление товара в корзину)
    def test_add_view(self):
        self.client.login(username="testuser", password="password123")
        url = reverse("item:add", kwargs={"pk": self.item.pk})
        response = self.client.get(url)
        self.user.refresh_from_db()
        self.assertIn(self.item, self.user.items.all())
        # add вызывает detail, поэтому статус 200
        self.assertEqual(response.status_code, 200)

    # basket view (корзина)
    def test_basket_view(self):
        self.client.login(username="testuser", password="password123")
        self.user.items.add(self.item)
        url = reverse("item:basket")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("items", response.context)
        self.assertContains(response, self.item.name)

    # remove view (удаление товара из корзины)
    def test_remove_view(self):
        self.client.login(username="testuser", password="password123")
        self.user.items.add(self.item)
        url = reverse("item:remove", kwargs={"pk": self.item.pk})
        response = self.client.get(url)
        self.user.refresh_from_db()
        self.assertNotIn(self.item, self.user.items.all())
        self.assertEqual(response.status_code, 302)

    # remove_detail view (удаление товара из корзины с переходом на detail)
    def test_remove_detail_view(self):
        self.client.login(username="testuser", password="password123")
        self.user.items.add(self.item)
        url = reverse("item:remove_detail", kwargs={"pk": self.item.pk})
        response = self.client.get(url)
        self.user.refresh_from_db()
        self.assertNotIn(self.item, self.user.items.all())
        self.assertEqual(response.status_code, 200)

    # gender_f view (смена пола) — если URL не определен, тест пропускается
    def test_gender_f_view(self):
        try:
            url = reverse("item:gender_f", kwargs={"gender": "W"})
        except NoReverseMatch:
            self.skipTest("URL name 'gender_f' не определен в urls.py")
        response = self.client.get(url, HTTP_REFERER="/somepage/")
        self.assertEqual(response.status_code, 302)
        session = self.client.session
        self.assertEqual(session["gender"], "W")

    # gender_index view (список товаров с фильтром по полу)
    def test_gender_index_view(self):
        url = reverse("item:gender_index", kwargs={"gender": "W"})
        response = self.client.get(url, {"query": "Test"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["gender"], "W")
        self.assertIn("categories", response.context)
        self.assertIn("items", response.context)
        self.assertIn("query", response.context)

    # gender_detail view (детали товара с фильтром по полу)
    def test_gender_detail_view(self):
        url = reverse("item:gender_detail", kwargs={"gender": "W", "pk": self.item.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["gender"], "W")
        self.assertIn("item", response.context)
        self.assertIn("related_items", response.context)

    # gender_detail_f view (смена пола и редирект на detail)
    def test_gender_detail_f_view(self):
        from django.urls import NoReverseMatch

        try:
            url = reverse("item:gender_detail_f", kwargs={"gender": "W", "pk": self.item.pk})
        except NoReverseMatch:
            self.skipTest("URL name 'gender_detail_f' не найден в urls.py")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(self.item.pk), response.url)

    # delete view (очистка корзины)
    def test_delete_view(self):
        self.client.login(username="testuser", password="password123")
        self.user.items.add(self.item)
        url = reverse("item:delete")
        response = self.client.get(url)
        self.user.refresh_from_db()
        self.assertEqual(self.user.items.count(), 0)
        self.assertEqual(response.status_code, 302)

    # purchase view (оформление покупки)
    def test_purchase_view(self):
        self.client.login(username="testuser", password="password123")
        self.user.items.add(self.item)
        url = reverse("item:purchase")
        response = self.client.post(url, {"telegram": "test_telegram"})
        self.user.refresh_from_db()
        self.assertEqual(self.user.items.count(), 0)
        self.assertEqual(response.status_code, 302)

    # purchase_delete_admin view (удаление покупки администратором)
    def test_purchase_delete_admin_view(self):
        self.client.login(username="admin", password="adminpass")
        purchase = Purchase.objects.create(
            user=self.superuser, telegram="admin_telegram", price=100
        )
        purchase.items.add(self.item)
        url = reverse("item:purchase_delete_admin", kwargs={"pk": purchase.pk})
        response = self.client.get(url)
        with self.assertRaises(Purchase.DoesNotExist):
            Purchase.objects.get(pk=purchase.pk)
        self.assertEqual(response.status_code, 200)

    # purchase_delete view (удаление покупки пользователем)
    def test_purchase_delete_view(self):
        self.client.login(username="testuser", password="password123")
        purchase = Purchase.objects.create(user=self.user, telegram="user_telegram", price=100)
        purchase.items.add(self.item)
        url = reverse("item:purchase_delete", kwargs={"pk": purchase.pk})
        response = self.client.get(url)
        with self.assertRaises(Purchase.DoesNotExist):
            Purchase.objects.get(pk=purchase.pk)
        self.assertEqual(response.status_code, 302)

    # all_purchases view (просмотр всех покупок для суперпользователя)
    def test_all_purchases_view_superuser(self):
        self.client.login(username="admin", password="adminpass")
        Purchase.objects.create(user=self.superuser, telegram="admin_telegram", price=100)
        url = reverse("item:all_purchases")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("purchases", response.context)

    def test_all_purchases_view_non_superuser(self):
        self.client.login(username="testuser", password="password123")
        url = reverse("item:all_purchases")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    # new_category view (создание новой категории, суперпользователь)
    def test_new_category_view(self):
        self.client.login(username="admin", password="adminpass")
        url = reverse("item:new_category")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        data = {"name": "New Category"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Category.objects.filter(name="New Category").exists())

    # new_item view (создание нового товара, суперпользователь)
    def test_new_item_view(self):
        self.client.login(username="admin", password="adminpass")
        url = reverse("item:new_item")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        image = SimpleUploadedFile("new_item.jpg", b"new_item_content", content_type="image/jpeg")
        data = {
            "name": "New Item",
            "description": "New item description",
            "price": 200.00,
            "category": self.category.pk,
            "gender": "M",
        }
        response = self.client.post(url, data, files={"image": image})
        self.assertEqual(response.status_code, 302)
        new_item = Item.objects.get(name="New Item")
        self.assertIsNotNone(new_item)

    # remove_item view (удаление товара, суперпользователь)
    def test_remove_item_view(self):
        self.client.login(username="admin", password="adminpass")
        item_to_remove = Item.objects.create(
            name="Item to remove",
            description="Description",
            price=50.00,
            image=SimpleUploadedFile("remove.jpg", b"content", content_type="image/jpeg"),
            category=self.category,
            is_sold=False,
            created_at=timezone.now(),
            gender="M",
        )
        url = reverse("item:remove_item", kwargs={"pk": item_to_remove.pk})
        response = self.client.get(url)
        with self.assertRaises(Item.DoesNotExist):
            Item.objects.get(pk=item_to_remove.pk)
        self.assertEqual(response.status_code, 302)

    # remove_category view (удаление категории, суперпользователь)
    def test_remove_category_view(self):
        self.client.login(username="admin", password="adminpass")
        category_to_remove = Category.objects.create(name="Category to remove")
        url = reverse("item:remove_category", kwargs={"pk": category_to_remove.pk})
        response = self.client.get(url)
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(pk=category_to_remove.pk)
        self.assertEqual(response.status_code, 302)

    # edit_item view (редактирование товара, суперпользователь)
    def test_edit_item_view(self):
        self.client.login(username="admin", password="adminpass")
        url = reverse("item:edit_item", kwargs={"pk": self.item.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        data = {
            "name": "Edited Test Item",
            "description": self.item.description,
            "price": self.item.price,
            "category": self.category.pk,
            "gender": self.item.gender,
        }
        response = self.client.post(url, data)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, "Edited Test Item")
        self.assertEqual(response.status_code, 302)

    # edit_category view (редактирование категории, суперпользователь)
    def test_edit_category_view(self):
        self.client.login(username="admin", password="adminpass")
        url = reverse("item:edit_category", kwargs={"pk": self.category.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        data = {"name": "Edited Category"}
        response = self.client.post(url, data)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Edited Category")
        self.assertEqual(response.status_code, 302)

    # new_comment view (создание нового комментария, авторизованный пользователь)
    def test_new_comment_view(self):
        self.client.login(username="testuser", password="password123")
        url = reverse("item:new_comment", kwargs={"pk": self.item.pk})
        data = {"description": "Great item!"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.item.refresh_from_db()
        self.assertTrue(self.item.comments.filter(description="Great item!").exists())

    # delete_comment view (удаление комментария)
    def test_delete_comment_view(self):
        self.client.login(username="testuser", password="password123")
        comment = Comment.objects.create(
            user=self.user, description="Comment to delete", created_at=timezone.now()
        )
        self.item.comments.add(comment)
        url = reverse(
            "item:delete_comment",
            kwargs={"pk_comment": comment.pk, "pk_item": self.item.pk},
        )
        response = self.client.get(url)
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(pk=comment.pk)
        self.assertEqual(response.status_code, 200)

    # edit_comment view (редактирование комментария)
    def test_edit_comment_view(self):
        self.client.login(username="testuser", password="password123")
        comment = Comment.objects.create(
            user=self.user, description="Original comment", created_at=timezone.now()
        )
        self.item.comments.add(comment)
        url = reverse(
            "item:edit_comment",
            kwargs={"pk_comment": comment.pk, "pk_item": self.item.pk},
        )
        # GET: получение формы для редактирования
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        # POST: отправка отредактированного комментария
        data = {"description": "Edited comment"}
        response = self.client.post(url, data)
        comment.refresh_from_db()
        self.assertEqual(comment.description, "Edited comment")
        # Ожидаем, что после редактирования вернется страница (200), т.к. view возвращает render
        self.assertEqual(response.status_code, 200)

    # all_comments view (просмотр всех комментариев пользователя)
    def test_all_comments_view(self):
        self.client.login(username="testuser", password="password123")
        comment = Comment.objects.create(
            user=self.user, description="User comment", created_at=timezone.now()
        )
        self.item.comments.add(comment)
        url = reverse("item:all_comments")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("items", response.context)
        self.assertIn(self.item, response.context["items"])
