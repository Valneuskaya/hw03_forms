from django.core.paginator import Paginator

from django.shortcuts import get_object_or_404, render, redirect

from .models import Group, Post, User

from .forms import PostForm

from django.contrib.auth.decorators import login_required


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/index.html'
    context = {'posts': posts, 'page_obj': page_obj, }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    # Здесь код запроса к модели и создание словаря контекста
    user = get_object_or_404(User, username=username)
    posts = user.group_posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/profile.html'
    title = 'Профайл пользователя ' + username
    context = {
        'title': title,
        'page_obj': page_obj,
        'posts': posts,
        'user': user,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    group = Group.objects.filter(title=post.group).first()
    count = Post.objects.filter(author=post.author).count()
    title = 'Пост '
    template = 'posts/post_detail.html'
    context = {
        'post': post,
        'count': count,
        'title': title,
        'group': group,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    groups = Group.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(f'/profile/{post.author}/',
                            {'form': form, 'groups': groups})
    form = PostForm()
    template = 'posts/create_post.html'
    return render(request, template, {'form': form, 'groups': groups})


@login_required
def post_edit(request, post_id):
    is_edit = True
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post.author = request.user
            post.pk = post_id
            post.text = form.cleaned_data['text']
            template = 'posts:post_detail'
            post.save()
            return redirect(template, post_id=post.pk)
    else:
        groups = Group.objects.all()
        form = PostForm(instance=post)
        template = 'posts/create_post.html'
    context = {
        'form': form,
        'groups': groups,
        'is_edit': is_edit
    }
    return render(request, template, context)
