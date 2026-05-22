from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    subscriptions = models.ManyToManyField(
        User,
        related_name='subscribers',
        blank=True
    )

    def __str__(self):
        return self.user.username


class Post(models.Model):
    ACCESS_PUBLIC = 'public'
    ACCESS_PRIVATE = 'private'
    ACCESS_CHOICES = [
        (ACCESS_PUBLIC, 'Публичный'),
        (ACCESS_PRIVATE, 'По запросу'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    access = models.CharField(max_length=10, choices=ACCESS_CHOICES, default=ACCESS_PUBLIC, verbose_name='Доступ')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Тэги')

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} → {self.post.title}'
    
    
class AccessRequest(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Ожидает'),
        (STATUS_APPROVED, 'Одобрен'),
        (STATUS_REJECTED, 'Отклонён'),
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='access_requests')
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='access_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        
        unique_together = ('post', 'requester')

    def __str__(self):
        return f'{self.requester.username} → {self.post.title} ({self.status})'