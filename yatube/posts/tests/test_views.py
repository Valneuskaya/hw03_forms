from django.test import TestCase, Client

from django.urls import reverse
from django import forms

from posts.models import User, Group, Post


class PostViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='Lera')
        cls.group_1 = Group.objects.create(
            title='test_group_title_1',
            slug='test_slug_1',
            description='test_description_1',
        )
        cls.group_2 = Group.objects.create(
            title='test_group_title_2',
            slug='test_slug_2',
            description='test_description_2',
        )
        cls.post = Post.objects.create(
            text='test_text',
            pub_date='test_date',
            author=cls.author,
            group=cls.group_1
        )

    def setUp(self):
        # Создаем неавторизованного пользователя
        self.guest_client = Client()
        # Создаем авторизованного пользователя
        self.user = User.objects.create_user(username='NoName')
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """Тест: URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
        templates_page_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': reverse('posts:group_list', kwargs={
                'slug': PostViewTests.group_1.slug}),
            'posts/profile.html': reverse('posts:profile', kwargs={
                'username': PostViewTests.author.username}),
            'posts/post_detail.html': reverse('posts:post_detail', kwargs={
                'post_id': PostViewTests.post.id}),
            'posts/create_post.html': reverse('posts:post_edit', kwargs={
                'post_id': PostViewTests.post.id}),
        }
        # Проверяем, что при обращении к name
        # вызывается соответствующий HTML-шаблон
        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        context = response.context['page_obj'][0]
        index_text_0 = context.text
        index_author_0 = context.author
        index_group_0 = context.group
        self.assertEqual(index_text_0, 'test_text')
        self.assertEqual(index_author_0, PostViewTests.author)
        self.assertEqual(index_group_0, PostViewTests.group_1)

    def test_group_list_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.guest_client.get(reverse('posts:group_list', kwargs={
            'slug': PostViewTests.group_1.slug}))
        context = response.context['page_obj'][0]
        post_text_0 = context.text
        post_group_0 = context.group
        self.assertEqual(post_text_0, 'test_text')
        self.assertEqual(post_group_0, self.group_1)

    def test_profile_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:profile', kwargs={
            'username': PostViewTests.author.username}))
        context = response.context['page_obj'][0]
        post_text_0 = context.text
        post_author_0 = context.author
        self.assertEqual(post_text_0, PostViewTests.post.text)
        self.assertEqual(post_author_0, PostViewTests.author)

    def test_post_detail_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={
                'post_id': PostViewTests.post.id}))
        self.assertEqual(
            response.context['post'].text, 'test_text'
        )

    def test_create_post_show_correct_context(self):
        """Шаблон create_post сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        # Словарь ожидаемых типов полей формы:
        # указываем, объектами какого класса должны быть поля формы
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }
        # Проверяем, что типы полей формы в словаре context
        # соответствуют ожиданиям
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                # Проверяет, что поле формы является экземпляром
                # указанного класса
                self.assertIsInstance(form_field, expected)

    def test_edit_post_show_correct_context(self):
        """Шаблон edit_post сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:post_edit', kwargs={'post_id': PostViewTests.post.id}))
        # Словарь ожидаемых типов полей формы:
        # указываем, объектами какого класса должны быть поля формы
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }
        # Проверяем, что типы полей формы в словаре context
        # соответствуют ожиданиям
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                # Проверяет, что поле формы является экземпляром
                # указанного класса
                self.assertIsInstance(form_field, expected)

    def test_post_is_on_pages(self):
        response_1 = self.authorized_client.get(reverse('posts:index'))
        response_2_1 = self.authorized_client.get(reverse('posts:group_list', kwargs={
            'slug': PostViewTests.group_1.slug}))
        response_2_2 = self.authorized_client.get(reverse('posts:group_list', kwargs={
            'slug': PostViewTests.group_2.slug}))
        response_3 = self.authorized_client.get(reverse('posts:profile', kwargs={
            'username': PostViewTests.author.username}))
        for response in [response_1, response_2_1, response_3]:
            context = response.context['page_obj'][0]
            post_text = context.text
            post_author = context.author
            post_group = context.group
            self.assertTrue(PostViewTests.post in response.context['page_obj'])
            self.assertEqual(post_text, PostViewTests.post.text)
            self.assertEqual(post_author, PostViewTests.author)
            self.assertEqual(post_group, PostViewTests.group_1)
        # пост не попал в группу, для которой не был предназначен
        self.assertTrue(PostViewTests.post not in response_2_2.context['page_obj'])


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.page_obj = []
        cls.author = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='test_group_title',
            slug='test_slug',
            description='test_description',
        )
        for i in range(13):
            cls.page_obj.append(
                Post(
                    author=cls.author,
                    text=f'{i} test_text',
                    group=cls.group,
                )
            )
        cls.posts = Post.objects.bulk_create(cls.page_obj)

    def setUp(self):
        # Создаем неавторизованного пользователя
        self.guest_client = Client()

    def test_index_first_page_contains_ten_records(self):
        """Тест: на первой странице index должно быть 10 постов."""
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_index_second_page_contains_three_records(self):
        """Тест: на второй странице index должно быть три поста."""
        response = self.client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_group_list_first_page_contains_ten_records(self):
        """Тест: на первой странице group_list должно быть 10 постов."""
        response = self.client.get(reverse('posts:group_list', kwargs={
            'slug': PaginatorViewsTest.group.slug}))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_group_list_second_page_contains_three_records(self):
        """Тест: на второй странице group_list должно быть три поста."""
        response = self.client.get(reverse('posts:group_list', kwargs={
            'slug': PaginatorViewsTest.group.slug}) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_profile_first_page_contains_ten_records(self):
        """Тест: на первой странице profile должно быть 10 постов."""
        response = self.client.get(reverse('posts:profile', kwargs={
            'username': PaginatorViewsTest.author.username}))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_profile_second_page_contains_three_records(self):
        """Тест: на второй странице profile должно быть три поста."""
        response = self.client.get(reverse('posts:profile', kwargs={
            'username': PaginatorViewsTest.author.username}) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)
