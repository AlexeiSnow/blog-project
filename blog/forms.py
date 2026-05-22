from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Post, Comment


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']


class EditAccountForm(forms.Form):
    username = forms.CharField(max_length=150, label='Логин')
    email = forms.EmailField(label='Email')
    new_password = forms.CharField(
        widget=forms.PasswordInput, label='Новый пароль', required=False
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, label='Повторите пароль', required=False
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['username'].initial = user.username
        self.fields['email'].initial = user.email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError('Этот логин уже занят')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError('Этот email уже используется')
        return email

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        if new_password and new_password != confirm_password:
            self.add_error('confirm_password', 'Пароли не совпадают')
        return cleaned_data


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'access', 'tags']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']