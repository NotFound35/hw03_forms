from django.core.paginator import Paginator

from django.shortcuts import render, get_object_or_404, redirect

from .models import Post, Group, User


from .forms import PostForm

from django.contrib.auth.decorators import login_required

POST_COUNT = 10
# Create your views here.


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group)
    page = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = page.get_page(page_number)
    context = {
        "group": group,
        "posts": posts,
        'page_obj': page_obj
    }
    return render(request, "posts/group_list.html", context)


def profile(request, username):
    template_name = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author_id=author)
    page = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = page.get_page(page_number)
    post_count = Post.objects.filter(author__username=username).count()
    context = {
        'page_obj': page_obj,
        'post_count': post_count,
        'author': author
    }
    return render(request, template_name, context)


def post_detail(request, post_id):
    template_name = 'posts/post_detail.html'
    post = get_object_or_404(Post, id=post_id)
    username = get_object_or_404(User, id=post.author_id)
    post_count = Post.objects.filter(author__username=username).count()
    author = get_object_or_404(User, username=username)
    context = {
        'post': post,
        'username': username,
        'post_count': post_count,
        'author': author
    }
    return render(request, template_name, context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', post.author)
    form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    is_edit = True
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return redirect('posts:post_detail', post_id)
        context = {
            'form': form,
            'post': post
        }
        return render(request, 'posts/create_post.html', context)
    else:
        form = PostForm(instance=post)
        context = {
            'form': form,
            'post': post,
            'is_edit': is_edit
        }
        return render(request, 'posts/create_post.html', context)
