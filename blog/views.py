from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Tag
from .forms import RegisterForm, ProfileForm, PostForm, CommentForm, EditAccountForm


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'blog/login.html', {'error': 'Неверный логин или пароль'})
    return render(request, 'blog/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def subscribe_view(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    profile = request.user.profile
    if target_user in profile.subscriptions.all():
        profile.subscriptions.remove(target_user)
    else:
        profile.subscriptions.add(target_user)
    return redirect(f'/user/{user_id}/')


def index_view(request):
    tag_id = request.GET.get('tag')
    posts = Post.objects.filter(access=Post.ACCESS_PUBLIC)
    if tag_id:
        posts = posts.filter(tags__id=tag_id)
    posts = posts.order_by('-created_at')
    tags = Tag.objects.all().order_by('name')
    return render(request, 'blog/index.html', {
        'posts': posts,
        'tags': tags,
        'selected_tag': int(tag_id) if tag_id and tag_id.isdigit() else None,
    })


def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.access == Post.ACCESS_PRIVATE and request.user != post.author:
        has_access = False
        existing_request = None

        if request.user.is_authenticated:
            try:
                existing_request = AccessRequest.objects.get(post=post, requester=request.user)
                has_access = existing_request.status == AccessRequest.STATUS_APPROVED
            except AccessRequest.DoesNotExist:
                pass

        if not has_access:
            return render(request, 'blog/private.html', {
                'post': post,
                'existing_request': existing_request,
            })

    comments = post.comments.all().order_by('created_at')
    comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })


@login_required
def post_create_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect(f'/post/{post.id}/')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Новый пост'})


@login_required
def post_edit_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    
    if request.user != post.author:
        return redirect(f'/post/{post.id}/')
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect(f'/post/{post.id}/')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Редактировать пост'})


@login_required
def post_delete_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    
    if request.user != post.author:
        return redirect(f'/post/{post.id}/')
    
    if request.method == 'POST':
        post.delete()
        return redirect('/')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


def user_profile_view(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    
    
    if request.user == profile_user:
        posts = Post.objects.filter(author=profile_user).order_by('-created_at')
    else:
        posts = Post.objects.all().filter(author=profile_user).order_by('-created_at')
    
    is_subscribed = False
    if request.user.is_authenticated:
        is_subscribed = profile_user in request.user.profile.subscriptions.all()
    
    return render(request, 'blog/user_profile.html', {
        'profile_user': profile_user,
        'posts': posts,
        'is_subscribed': is_subscribed,
    })


@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = EditAccountForm(request.user, request.POST)
        if form.is_valid():
            request.user.username = form.cleaned_data['username']
            request.user.email = form.cleaned_data['email']
            if form.cleaned_data['new_password']:
                request.user.set_password(form.cleaned_data['new_password'])
            request.user.save()
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, request.user)
            from django.contrib import messages
            messages.success(request, 'Профиль успешно обновлён')
            return redirect(f'/user/{request.user.id}/')
    else:
        form = EditAccountForm(request.user)
    return render(request, 'blog/profile_edit.html', {'form': form})


@login_required
def comment_add_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect(f'/post/{post_id}/')


@login_required
def comment_delete_view(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)


    if request.user == comment.author:
        post_id = comment.post.id
        comment.delete()
        return redirect(f'/post/{post_id}/')
    return redirect('/')


@login_required
def feed_view(request):
    subscriptions = request.user.profile.subscriptions.all()
    tag_id = request.GET.get('tag')
    posts = Post.objects.filter(author__in=list(subscriptions) + [request.user])
    if tag_id:
        posts = posts.filter(tags__id=tag_id)
    posts = posts.order_by('-created_at')
    tags = Tag.objects.all().order_by('name')
    return render(request, 'blog/feed.html', {
        'posts': posts,
        'tags': tags,
        'selected_tag': int(tag_id) if tag_id and tag_id.isdigit() else None,
    })


@login_required
def tag_create_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            from .models import Tag
            Tag.objects.get_or_create(name=name)
        return redirect('/tags/')
    return render(request, 'blog/tag_create.html')


def tag_list_view(request):
    from .models import Tag
    tags = Tag.objects.all().order_by('name')
    return render(request, 'blog/tag_list.html', {'tags': tags})


def tag_posts_view(request, tag_id):
    from .models import Tag
    tag = get_object_or_404(Tag, id=tag_id)
    posts = Post.objects.filter(
        tags=tag,
        access=Post.ACCESS_PUBLIC
    ).order_by('-created_at')
    return render(request, 'blog/tag_posts.html', {'tag': tag, 'posts': posts})

import json
from django.http import JsonResponse


@login_required
def tag_create_ajax_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        if not name:
            return JsonResponse({'success': False, 'error': 'Название не может быть пустым'})
        from .models import Tag
        tag, created = Tag.objects.get_or_create(name=name)
        return JsonResponse({'success': True, 'id': tag.id, 'name': tag.name})
    return JsonResponse({'success': False, 'error': 'Неверный запрос'})

from .models import AccessRequest


@login_required
def access_request_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author == request.user:
        return redirect(f'/post/{post_id}/')
    AccessRequest.objects.get_or_create(post=post, requester=request.user)
    return redirect(f'/post/{post_id}/')


@login_required
def access_requests_list_view(request):
    requests = AccessRequest.objects.filter(
        post__author=request.user,
        status=AccessRequest.STATUS_PENDING
    ).order_by('-created_at')
    return render(request, 'blog/access_requests.html', {'requests': requests})


@login_required
def access_request_action_view(request, request_id, action):
    access_request = get_object_or_404(AccessRequest, id=request_id, post__author=request.user)
    if action == 'approve':
        access_request.status = AccessRequest.STATUS_APPROVED
    elif action == 'reject':
        access_request.status = AccessRequest.STATUS_REJECTED
    access_request.save()
    return redirect('/requests/')