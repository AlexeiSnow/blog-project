from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('subscribe/<int:user_id>/', views.subscribe_view, name='subscribe'),
    path('post/create/', views.post_create_view, name='post_create'),
    path('post/<int:post_id>/', views.post_detail_view, name='post_detail'),
    path('post/<int:post_id>/edit/', views.post_edit_view, name='post_edit'),
    path('post/<int:post_id>/delete/', views.post_delete_view, name='post_delete'),
    path('user/<int:user_id>/', views.user_profile_view, name='user_profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('post/<int:post_id>/comment/', views.comment_add_view, name='comment_add'),
    path('comment/<int:comment_id>/delete/', views.comment_delete_view, name='comment_delete'),
    path('feed/', views.feed_view, name='feed'),
    path('tags/', views.tag_list_view, name='tag_list'),
    path('tags/create/', views.tag_create_view, name='tag_create'),
    path('tags/<int:tag_id>/', views.tag_posts_view, name='tag_posts'), 
    path('tags/create/ajax/', views.tag_create_ajax_view, name='tag_create_ajax'),
    path('post/<int:post_id>/request/', views.access_request_view, name='access_request'),
    path('requests/', views.access_requests_list_view, name='access_requests'),
    path('requests/<int:request_id>/<str:action>/', views.access_request_action_view, name='access_request_action'),
]