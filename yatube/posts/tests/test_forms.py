from django.test import TestCase, Client
from posts.forms import PostForm


from django.urls import reverse

from posts.models import User, Group, Post


class CreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='Lera')
        cls.group = Group.objects.create(
            title='test_group_title',
            slug='test_slug',
            description='test_description',
        )
        cls.post = Post.objects.create(
            text='test_text',
            pub_date='test_date',
            author=cls.author,
            group=cls.group
        )
        cls.form = PostForm()

    def setUp(self):
        # Создаем неавторизованного пользователя
        self.guest_client = Client()
        # Создаем авторизованного пользователя
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.author)

    def test_create_task(self):
        """Тест на создание новой записи в базе данных"""
        # Подсчитаем количество записей в Post
        post_count = Post.objects.count()
        form_data = {
            'text': 'test_text',
            'id_group': CreateFormTests.group.pk,
        }
        # Отправляем POST-запрос
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        # print(response.content.decode())
        # Прверяем редирект
        self.assertRedirects(response, reverse('posts:profile', kwargs={
            'username': self.author.username}))
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), post_count + 1)
        # Проверим, что ничего не упало и страница отдаёт код 200
        # self.assertEqual(response.status_code, 200)

    def test_edit_task(self):
        """Тест на редактирование записи в базе данных"""
        # Подсчитаем количество записей в Post
        post_count = Post.objects.count()
        # Проверяем исходный текст
        self.assertEquals('test_text', Post.objects.filter(pk=CreateFormTests.post.id)[0].text)
        # Изменяем текст
        form_data = {
            'text': 'test_text edit',
            'id_group': CreateFormTests.group.pk,
        }
        # Отправляем POST-запрос
        response = self.authorized_client.post(reverse('posts:post_edit', kwargs={
            'post_id': CreateFormTests.post.id}),
            data=form_data,
            follow=True
        )
        # print(response.content.decode())
        # Прверяем редирект
        self.assertRedirects(response, reverse('posts:post_detail', kwargs={
            'post_id': CreateFormTests.post.id}))
        # Проверяем измененный текст
        self.assertEquals('test_text edit', Post.objects.filter(pk=CreateFormTests.post.id)[0].text)
        # Проверяем число постов
        self.assertEqual(Post.objects.count(), post_count)
        # Проверим, что ничего не упало и страница отдаёт код 200
        # self.assertEqual(response.status_code, 200)
