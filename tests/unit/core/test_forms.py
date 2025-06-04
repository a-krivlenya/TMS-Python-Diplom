from django.contrib.auth.models import User
from django.test import TestCase

from core.forms import LoginForm, SignupForm


class LoginFormTestCase(TestCase):
    def setUp(self):
        """Создаем пользователя перед тестами"""
        self.user = User.objects.create_user(username="testuser", password="securepassword")

    def test_login_form_valid(self):
        """Форма логина должна быть валидной при корректных данных"""
        form_data = {"username": "testuser", "password": "securepassword"}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        """Форма логина должна быть невалидной при отсутствии данных"""
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertIn("password", form.errors)

    def test_login_form_widget_attrs(self):
        """Проверяем кастомные атрибуты полей формы логина"""
        form = LoginForm()
        self.assertEqual(form.fields["username"].widget.attrs["placeholder"], "Your username")
        self.assertEqual(form.fields["password"].widget.attrs["placeholder"], "Your password")


class SignupFormTestCase(TestCase):
    def test_signup_form_valid(self):
        """Форма регистрации должна быть валидной при корректных данных"""
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        }
        form = SignupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_signup_form_password_mismatch(self):
        """Форма должна быть невалидной, если пароли не совпадают"""
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "StrongPass123!",
            "password2": "WrongPass123!",
        }
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_signup_form_missing_fields(self):
        """Форма регистрации должна быть невалидной, если отсутствуют обязательные поля"""
        form = SignupForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertIn("email", form.errors)
        self.assertIn("password1", form.errors)
        self.assertIn("password2", form.errors)

    def test_signup_form_widget_attrs(self):
        """Проверяем кастомные атрибуты полей формы регистрации"""
        form = SignupForm()
        self.assertEqual(form.fields["username"].widget.attrs["placeholder"], "Your username")
        self.assertEqual(form.fields["email"].widget.attrs["placeholder"], "Your email address")
        self.assertEqual(form.fields["password1"].widget.attrs["placeholder"], "Your password")
        self.assertEqual(form.fields["password2"].widget.attrs["placeholder"], "Repeat password")
