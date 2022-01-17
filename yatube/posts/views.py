from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User


@require_http_methods(["GET"])
def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/index.html'
    context = {'page_obj': page_obj, }
    return render(request, template, context)


@require_http_methods(["GET"])
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.group_posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/group_list.html'
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


@require_http_methods(["GET"])
def profile(request, username):
    # Здесь код запроса к модели и создание словаря контекста
    author = get_object_or_404(User, username=username)
    posts = author.group_posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/profile.html'
    context = {
        'page_obj': page_obj,
        'author': author,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    count = Post.objects.filter(author=post.author).count()
    template = 'posts/post_detail.html'
    context = {
        'post': post,
        'count': count,
    }
    return render(request, template, context)


@login_required
@require_http_methods(["GET", "POST"])
def post_create(request):
    groups = Group.objects.all()
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=post.author.username)
    template = 'posts/create_post.html'
    return render(request, template, {'form': form, 'groups': groups})


@login_required
@require_http_methods(["GET", "POST"])
def post_edit(request, post_id):
    is_edit = True
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        template = 'posts:post_detail'
        post.save()
        return redirect(template, post_id=post.pk)
    groups = Group.objects.all()
    template = 'posts/create_post.html'
    context = {
        'form': form,
        'groups': groups,
        'is_edit': is_edit
    }
    return render(request, template, context)
