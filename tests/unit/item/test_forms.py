import io

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone
from PIL import Image

from item.forms import (
    EditCategoryForm,
    EditItemForm,
    NewCategoryForm,
    NewCommentForm,
    NewItemForm,
)
from item.models import Category, Comment, Item


class FormTests(TestCase):
    def setUp(self):
        # Create a user first
        self.user = User.objects.create_user(username="testuser", password="password")

        # Create other objects like Category and Item
        self.category = Category.objects.create(name="Test Category")
        self.item = Item.objects.create(
            category=self.category,
            name="Test Item",
            description="Test Description",
            price=10.0,
            image=None,
            gender="Unisex",
            is_sold=False,
        )

        # Now create the comment with the user
        self.comment = Comment.objects.create(
            item=self.item,
            description="Test Comment",
            created_at=timezone.now(),  # Explicitly setting the created_at field
            user=self.user,  # Assigning the user to the comment
        )

    def test_new_category_form_valid(self):
        form = NewCategoryForm(data={"name": "New Category"})
        self.assertTrue(form.is_valid())

    def test_new_category_form_invalid(self):
        form = NewCategoryForm(data={})
        self.assertFalse(form.is_valid())

    def test_new_comment_form_valid(self):
        form = NewCommentForm(data={"description": "A new comment"})
        self.assertTrue(form.is_valid())

    def test_new_comment_form_invalid(self):
        form = NewCommentForm(data={})
        self.assertFalse(form.is_valid())

        def test_new_item_form_valid(self):
            # A valid JPEG image header (this is just a basic example of JPEG bytes)
            image = SimpleUploadedFile(
                "test.jpg", b"\xff\xd8\xff\xe0\x00\x10JFIF", content_type="image/jpeg"
            )

            # Ensure 'gender' is a valid choice (e.g., 'M' for Male)
            form = NewItemForm(
                data={
                    "category": self.category.id,
                    "name": "New Item",
                    "description": "Description of item",
                    "price": 20.5,
                    "gender": "M",  # 'M' for Male, as defined in gender_choice
                },
                files={"image": image},
            )

            print(form.errors)  # Check form errors to debug
            self.assertTrue(form.is_valid())

    def test_new_item_form_invalid(self):
        form = NewItemForm(data={})
        self.assertFalse(form.is_valid())

    def test_edit_item_form_valid(self):
        # Create an in-memory image file
        img = Image.new("RGB", (100, 100), color="red")
        img_io = io.BytesIO()
        img.save(img_io, "JPEG")
        img_io.seek(0)

        image = SimpleUploadedFile("test.jpg", img_io.read(), content_type="image/jpeg")

        form = EditItemForm(
            data={
                "name": "Updated Item",
                "description": "Updated description",
                "price": 15.0,
                "is_sold": True,
                "gender": "M",  # Ensure this matches a valid option
            },
            files={"image": image},
        )

        print(form.errors)  # Check if any error exists
        self.assertTrue(form.is_valid())  # Ensure the form is valid

    def test_edit_item_form_invalid(self):
        form = EditItemForm(
            data={
                "name": "",
                "description": "",
                "price": "",  # empty price is likely invalid
                "is_sold": False,  # This field could be set to False as default, or you can set a valid boolean value
                "gender": "",  # Ensure gender field is populated correctly
            }
        )
        self.assertFalse(
            form.is_valid()
        )  # The form should be invalid due to missing or invalid data

    def test_edit_category_form_valid(self):
        form = EditCategoryForm(data={"name": "Updated Category"})
        self.assertTrue(form.is_valid())

    def test_edit_category_form_invalid(self):
        form = EditCategoryForm(data={"name": ""})
        self.assertFalse(form.is_valid())
