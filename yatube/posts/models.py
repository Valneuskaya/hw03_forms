from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField('Title', max_length=200)
    slug = models.SlugField('Slug', unique=True)
    description = models.TextField('Description')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Group'


class Post(models.Model):
    text = models.TextField('Text')
    pub_date = models.DateTimeField('Publication date', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='group_posts',
        verbose_name='Author')
    group = models.ForeignKey(
        Group,
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='group_posts',
        verbose_name='Group')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Post'
        ordering = ['-pub_date']
