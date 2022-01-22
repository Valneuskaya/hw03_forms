from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая группа',
        )

    def test_models_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        task_post = PostModelTest.post
        expected_post_name = task_post.text[:15]
        self.assertEqual(expected_post_name, str(task_post))
        task_group = PostModelTest.group
        expected_group_name = task_group.title
        self.assertEqual(expected_group_name, str(task_group))

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        task_post = PostModelTest.post
        field_verboses_post = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа',
        }
        for value, expected in field_verboses_post.items():
            with self.subTest(value=value):
                self.assertEqual(
                    task_post._meta.get_field(value).verbose_name, expected)
        task_group = PostModelTest.group
        field_verboses_group = {
            'title': 'Заголовок',
            'slug': 'Адрес страницы группы',
            'description': 'Описание',
        }
        for value, expected in field_verboses_group.items():
            with self.subTest(value=value):
                self.assertEqual(
                    task_group._meta.get_field(value).verbose_name, expected)
