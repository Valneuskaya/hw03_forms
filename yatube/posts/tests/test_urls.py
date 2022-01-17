# posts/tests/tests_url.py
from django.test import TestCase, Client


class StaticURLTests(TestCase):
    def setUp(self):
        # Устанавливаем данные для тестирования
        # Создаём экземпляр клиента. Он неавторизован.
        self.guest_client = Client()

    def test_homepage(self):
        # Отправляем запрос через client, созданный в setUp()
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_about_author(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_about_tech(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)
