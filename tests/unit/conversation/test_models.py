from django.contrib.auth.models import User
from django.test import TestCase

from conversation.models import Conversation, ConversationMessage
from item.models import Category, Item


class ConversationModelTestCase(TestCase):
    def setUp(self):
        """Создание тестовых данных"""
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")
        self.category = Category.objects.create(name="Test Category")
        self.item = Item.objects.create(
            name="Test Item",
            description="Test Description",
            price=10.0,
            category=self.category,  # Указываем категорию
        )

        self.conversation = Conversation.objects.create(item=self.item)
        self.conversation.members.set([self.user1, self.user2])  # Добавляем пользователей в чат

    def test_conversation_creation(self):
        """Тест: объект Conversation создается правильно"""
        self.assertEqual(self.conversation.item, self.item)
        self.assertEqual(self.conversation.members.count(), 2)

    def test_conversation_message_creation(self):
        """Тест: объект ConversationMessage создается и привязывается к чату"""
        message = ConversationMessage.objects.create(
            conversation=self.conversation, content="Hello!", created_by=self.user1
        )
        self.assertEqual(message.conversation, self.conversation)
        self.assertEqual(message.content, "Hello!")
        self.assertEqual(message.created_by, self.user1)

    def test_conversation_ordering(self):
        """Тест: чаты сортируются по modified_at (последнее измененное вверху)"""
        convo1 = Conversation.objects.create(item=self.item)
        convo2 = Conversation.objects.create(item=self.item)
        convo1.modified_at = "2024-03-01 12:00:00"
        convo2.modified_at = "2024-03-02 12:00:00"
        convo1.save()
        convo2.save()

        conversations = list(Conversation.objects.all())
        self.assertEqual(conversations[0], convo2)  # Должен быть сначала тот, что изменен позже
