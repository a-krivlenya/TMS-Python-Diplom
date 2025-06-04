from django.test import TestCase

from conversation.forms import ConversationMessageForm


class ConversationMessageFormTestCase(TestCase):
    def test_conversation_message_form_valid(self):
        """Форма должна быть валидной при корректных данных"""
        form_data = {"content": "Hello, this is a test message!"}
        form = ConversationMessageForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_conversation_message_form_invalid(self):
        """Форма должна быть невалидной, если поле content пустое"""
        form_data = {"content": ""}
        form = ConversationMessageForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)  # Убедимся, что ошибка связана с полем content
